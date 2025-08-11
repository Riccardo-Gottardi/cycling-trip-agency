# Context
## Bigger project
Develop an intelligent conversational systems for presonalized cycling trip planning.

## My task
Explore the feasibility of the creation of such a system, analizing methodologies of artificial intelligence applied to trip planning, steps optimization and base experience personalization based on the user preferences.

# To get started
## Get the code
```bash
git clone https://github.com/Riccardo-Gottardi/cycling-trip-agency
```

## Add environment variable
- In the root folder of the probect create a `.env` file
- Inside it place:
```
OPENAI_API_KEY:"<your-api-key>"
LOGFIRE_TOKEN:"<your-token>"
```
- `OPENAI_API_KEY` is required to access openai llm for the route planner agent. 
- Other llms provider can be used, you will need to:
    - Modify the file `crew.yaml` replacing, under the `llm` option, `openai:gpt-4.1-mini` with the desired one. 
    - Modify the api key name in `.env`
    
        (eg. if you want to use `groq:llama-3.3-70b-versatile`, write it in the crew.yaml, as described above, the api key in `.env` will be `GROQ_API_KEY`)

    More informations, about supported provider and more, can be found at: https://ai.pydantic.dev/models/
- `LOGFIRE_TOKEN`, is needed for debug purposes. Although it is not strictly required.

    More informations at: https://logfire.pydantic.dev/docs/how-to-guides/create-write-tokens/

## Setup the environment
- Create and activate a python virtual environment inside the project folder
- Follow the instructions at: https://docs.python.org/3/library/venv.html

Windows
```bash
pip install -r .\requirements.txt
```
Unix based/like
```bash
pip install -r ./requirements.txt
```

## Start a brouter server
- The program expect a brouter server at http://localhost:17777
- Follow the instructions at: https://github.com/abrensch/brouter

## Run the program
- Run the main.py

Windows
```bash
python .\main.py
```
Unix based/like
```bash
python3 ./main.py
```