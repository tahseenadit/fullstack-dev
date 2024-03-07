# Prerequisites

1. Postgresql installed and configured.
2. Node.js v16 or higher is installed.
3. You have your openai api key.


# How to run the API in the terminal ?

1. Open terminal\n
2. `cd` to backend\app directory\n
3. Execute `uvicorn main:app --reload` in the terminal\n
4. Open your browser and go to `http://127.0.0.1:8000`\n

# Interact with database

First, run fastapi by executing `uvicorn main:app --reload` in your terminal.

There are two functions implemented at the moment:\n
    1. Get all data\n
    2. Create data\n

## Get all data

Go to Postman and make a get request to the following url:\n
`http://127.0.0.1:8000\sample`

## Insert data

Go to Postman and make a get request to the following url:\n
`http://127.0.0.1:8000\sample\create`

Sample Body:\n
```
{
    "parameter": {
        "title": "Sample data",
        "description": "Sample description"
    }
}
```

# Get OpenAI response

1. Keep the backend running.
2. Open a new terminal and cd to frontend\my-app.
3. Run `npm start` in the terminal.
4. Go to the url `http:\\localhost:3000` in your browser.
5. Write your question in the first input area and click on Generate button.

# Get VertexAI response

1. Run `gcloud auth application-default login` in your terminal.
2. Start the backend if not running.
3. Keep the backend running.
4. Open a new terminal and cd to frontend\my-app.
5. Run `npm start` in the terminal.
6. Go to the url `http:\\localhost:3000` in your browser.
7. Write your question in the first input area and click on Generate button.
