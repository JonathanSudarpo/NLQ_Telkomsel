# app.py
from flask import Flask, render_template, request

from langchain.agents import create_pandas_dataframe_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.utilities import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain import PromptTemplate
from langchain.callbacks import StreamlitCallbackHandler
from langchain_experimental.sql import SQLDatabaseChain
import os
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
from urllib.parse import quote_plus

app = Flask(__name__)


# Set up the environment variables and instances for OpenAI
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_API_BASE"] = "https://networkgenai3.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

# Creating an OpenAI Chat LLM wrapper (Initialize it once)
llm = ChatOpenAI(temperature=0, deployment_id="gpt-35-turbo-0613")

# Create a SQLDatabase using the data (Initialize it once)
db = SQLDatabase.from_uri("postgresql://postgres:@localhost:5432/postgres")

# Creating a SQLDatabaseToolkit (Initialize it once)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

#PREFIX = "You're main task as an agent is to help with natural language query. When the user inputs a prompt, you are to reply in the format of 'You asked me (their question), the answer is (your answer)."

#ORMAT = "Append the SQL query you used to the FINAL answer after you parse the database and before you output"

# Creating a chat agent (Initialize it once)
agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

db_chain = SQLDatabaseChain.from_llm(ChatOpenAI(temperature=0, deployment_id="gpt-35-turbo-0613")
                                     , db
                                     , verbose=True
                                     , use_query_checker=True
                                     )

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

@app.route('/ndm_agents', methods=['GET', 'POST'])
def ndm_agents():

    chat_history = []  # Initialize chat history list

    if request.method == 'POST':
        prompt = request.form['user_input']
        option = request.form['option']

        if option == "create_sql_agent":
            response = agent.run(prompt)
        elif option == "SQLDatabaseChain":
            response = db_chain.run(prompt)
          # Append user's query and response to chat history with labels
        chat_history.append({"class": "user-message", "label": "User", "text": prompt})
        chat_history.append({"class": "assistant-message", "label": "Response", "text": response})

    return render_template('ndm_agents.html', chat_history=chat_history)

        #return render_template('ndm_agents.html', response=response)

  #  return render_template('ndm_agents.html', response=None)

if __name__ == '__main__':
    app.run(debug=True)

