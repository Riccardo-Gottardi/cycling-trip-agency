# Context
The current repository represent the project developed for my bachelor thesis, whose PDF is `thesis.pdf`

## Bigger project
Develop an intelligent conversational system for personalized cycling trip planning.

## My task
Explore the feasibility of the creation of such a system, analyzing methodologies of artificial intelligence applied to trip planning, steps optimization and base experience personalization based on the user preferences.

<br/>
<br/>

# Versions
The thesis was written based on an older version of the project, specifically the version of the commit of the October 6th, whose id is `59cde569211997f09d5317400d1af6eaf3ec1f6d`.

The project was then restructured due to usability issue. On the previous implementation the capability of LLMs weren't actually used.  

The current version have a smoother UX (User Experience) and produce a GPX file once terminated the planning process.

<br/>
<br/>

# To Get Started
## Get the code
```bash
git clone https://github.com/Riccardo-Gottardi/cycling-trip-agency
```

## Add Environment Variable
- In the root folder of the project create a `.env` file
- Inside it place:
```
OPENAI_API_KEY:"<your-api-key>"
LOGFIRE_TOKEN:"<your-token>"
```
- `OPENAI_API_KEY` is required to access openai llm for the route planner agent. 
- Other llms provider can be used, you will need to:
    - Modify the file `crew.yaml` replacing, under the `llm` option, `openai:gpt-4.1-mini` with the desired one. 
    - Modify the api key name in `.env`
    
        (e.g. if you want to use `groq:llama-3.3-70b-versatile`, write it in the crew.yaml, as described above, the api key in `.env` will be `GROQ_API_KEY`)

    More information, about supported provider and more, can be found at: https://ai.pydantic.dev/models/
- `LOGFIRE_TOKEN`, is needed for debug purposes. Although it is not strictly required.

    More information at: https://logfire.pydantic.dev/docs/how-to-guides/create-write-tokens/

## Setup the Environment
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

## Start a Brouter Server
- The program expect a brouter server at http://localhost:17777
- Follow the instructions at: https://github.com/abrensch/brouter

## Run the Program
- Run the main.py

Windows
```bash
python .\main.py
```
Unix based/like
```bash
python3 ./main.py
```