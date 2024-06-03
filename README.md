## How to Run

1. In a shell, set the OpenAI API Key as an environment variable OPENAI\_API\_KEY
2. Create a python virtualenv and pip install that packages from requirements.txt
3. Run python app.py, to start the backend server. Keep it running either in the background, or follow further steps in a different terminal. By default the backend server would start at http://localhost:5000
4. Change directory to frontend and run a simple python server, using "python -m http.server". Right now the frontend is just static html and js files, and hence could be directly opened in a browser (to test), or could be hosted in a python server, or something like Apache

## To change the backend hostname and port

1. In config.json, change the BACKEND\_HOST and BACKEND\_PORT
2. In frontend/index.js change the BACKEND\_SERVER variable to match the new host and port
