## App Demo URL : https://enterprise-workflow-advanced-rag-hackathon-happpfrjwtprwyzqsvw.streamlit.app/

# App Setup

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file:

# Add the following credentials in your .env file:

`VECTARA_CORUPS_NAME` = "YOUR_VECTARA_CORUPS_NAME"

`VECTARA_CLIENT_ID` = "YOUR_VECTARA_CLIENT_ID"

`VECTARA_SECRET` = "YOUR_VECTARA_SECRET"

`VECTARA_CUSTOMER_ID_SOP` = "YOUR_VECTARA_CUSTOMER_ID"

`VECTARA_API_KEY_SOP` = "YOUR_VECTARA_API_KEY"

`VECTARA_CUSTOMER_ID_SOP_CHAT` = "YOUR_VECTARA_CUSTOMER_ID"

`VECTARA_API_KEY_SOP_CHAT` = "YOUR_VECTARA_API_KEY"

`OPENAI_API_KEY` = "YOUR_OPENAI_API_KEY"

`TOGETHER_API_KEY` = "YOUR_TOGETHER_API_KEY"

`COHERE_API_KEY` = "YOUR_COHERE_API_KEY"

`WEAVIATE_HOST_SOP` = "YOUR_WEAVIATE_HOST_URL"

`WEAVIATE_HOST_SOP_CHAT` = "YOUR_WEAVIATE_HOST_URL"

`WEAVIATE_INDEX` = "YOUR_WEAVIATE_INDEX"

`TOGETHER_API_TOKEN` = "Bearer <YOUR_TOGETHER_API_TOKEN>"


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
