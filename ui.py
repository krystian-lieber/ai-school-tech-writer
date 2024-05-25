from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_chroma import Chroma
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.prompts.prompt import PromptTemplate

# Load environment variables
load_dotenv()

underlying_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

store = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)

loader = DirectoryLoader(
    path="data_ anticoagulant", glob="**/*.pdf", loader_cls=PyMuPDFLoader
)
documents = loader.load()
print(len(documents))
vectorstore = Chroma.from_documents(documents, cached_embedder)
# Set up the RetrievalQA chain
llm = ChatOpenAI(model="gpt-4o")
retriever = vectorstore.as_retriever()

# 2. Incorporate the retriever into a question-answering chain.
system_prompt = SystemMessage(
    content="""You are an assistant for question-answering tasks for medical professionals. 
    Use the retrieved context to answer the question. If you don't know the answer, say that you don't know. 
    Include the quotations from the relevant context to confirm the given information.
    Answer is the same language as the question.
    """
)
template = PromptTemplate(
    template="{query} Context: {context}", input_variables=["query", "context"]
)

temperature_slider = gr.Slider(minimum=0.0, maximum=1.0, value=0, label="Temperature")
max_tokens_slider = gr.Slider(minimum=1, maximum=4096, value=500, label="Max Tokens")


def respond_to_chat_with_controls(user_input, temperature, max_tokens):
    context = retriever.get_relevant_documents(user_input)
    prompt_with_context = template.format(query=user_input, context=context)
    print(prompt_with_context)
    messages = [system_prompt, HumanMessage(content=prompt_with_context)]
    result = llm(messages, temperature=temperature, max_tokens=max_tokens)
    return result.content


iface = gr.Interface(
    fn=respond_to_chat_with_controls,
    inputs=[
        gr.Textbox(lines=10, placeholder="Enter your query here..."),
        temperature_slider,
        max_tokens_slider,
    ],
    outputs=gr.Textbox(lines=10, placeholder="Response will appear here..."),
    title="Leki Antykrzepliwe",
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch()
