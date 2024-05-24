import os
import pickle
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def main():
    # Folder containing the PDF files
    data_dir = os.getenv("DATA_DIR", "data")
    characteristics_directory = f'{data_dir}/characteristics'

    # Load PDF files
    pdf_files = [f for f in os.listdir(characteristics_directory) if f.endswith('.pdf')]

    # Function to process a single PDF file
    def process_pdf(file_path):
        output_file = f'{file_path}.embeddings.pkl'
        if os.path.exists(output_file):
            return True
        try:
            # Load and split the PDF
            loader = PyMuPDFLoader(file_path)
            pages = loader.load_and_split()

            # Generate embeddings
            embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
            embedded_texts = [embeddings.embed_query(page.page_content) for page in pages]

            # Save embeddings to file
            with open(output_file, 'ab') as f:
                pickle.dump(embedded_texts, f)

            return True
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False

    # Initialize progress bar
    progress_bar = tqdm(total=len(pdf_files), unit='file', desc='Processing PDFs')

    # Create a thread pool with a maximum of 10 threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Prepare tasks for execution
        futures = [executor.submit(process_pdf, os.path.join(characteristics_directory, file)) for file in pdf_files]

        # Process the results as they become available
        for future in as_completed(futures):
            if future.result():
                progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

    print('Finished processing and saving embeddings.')

if __name__ == "__main__":
    main()