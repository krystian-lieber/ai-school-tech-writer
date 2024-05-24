# Polish Medicine Registry Q&A

## Overview

To change the topic from my day to day work I wanted to implement a system in which doctor's could ask questions and get answers from a database of medicine registered in Poland.

I used Langchain and OpenAI to implement this system. The first idea was to use the whole registry. But it was not possible to use the whole registry because it was too big. There are more than 13000 PDFs with multiple files each. The partial implementation can be found in the files:

 - dataloader.py - this file contains the code to load the data and download the PDFs with each product charasteristic.
 - embeddings.py - this file contains the code to create the embeddings for the data, the idea was to cache the embeddings on each for future use. 
 - vectorstore.py - this file contains the code to create the vector store.

 The limited scope included anticoagulant medicines, used to help patients with blood clotting problems. The system is not perfect, but it is a good example of how you can use Langchain to implement a system in which doctor's could ask questions and get answers from a database of medicine registered in Poland. 

 I used additional layer for caching embedding using `CacheBackedEmbeddings` to reduce the cost and improve startup time and `ChromaDB`. The UI is implemented using `Gradio`.

 To run the system install the requirements, set OPENAI_API_KEY and run the app.py file.

 ```bash
 pip install -r requirements.txt
 export OPENAI_API_KEY="your_openai_api_key"
 python app.py
 ```

