## App Demo URL : https://enterprise-workflow-advanced-rag-hackathon-happpfrjwtprwyzqsvw.streamlit.app/

# App Setup

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file:

`VECTARA_CLIENT_ID` = "YOUR VECTARA CLIENT ID"

`VECTARA_SECRET` = "YOUR VECTARA CLIENT SECRET"

`VECTARA_CUSTOMER_ID` = "YOUR VECTARA CUSTOMER ID"

`VECTARA_CORPUS_NAME` = "YOUR VECTARA CORPUS NAME"

`VECTARA_API_KEY` = "YOUR VECTARA API KEY"

`OPENAI_API_KEY` = "YOUR OPENAI API KEY"

`TOGETHER_API_KEY` = "YOUR TOGETHER API KEY"

`COHERE_API_KEY` = "YOUR COHERE API KEY"

`WEAVIATE_HOST` = "YOUR WEAVIATE HOST"

`WEAVIATE_INDEX` = "YOUR WEAVIATE INDEX"


## Installation

Ensure you have the following prerequisites installed:

- Python 3.10 or higher

Then, install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running streamlit application

```
streamlit run src/chatbot/streamlit.py
```
