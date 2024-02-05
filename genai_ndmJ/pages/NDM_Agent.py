# %%
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
import streamlit as st

# Set up the environment variables and instances for OpenAI
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = OPEN_API_KEY
os.environ["OPENAI_API_BASE"] = "https://networkgenai3.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"  

# Creating an OpenAI Chat LLM wrapper
llm = ChatOpenAI(temperature=0, deployment_id="gpt-35-turbo-0613")

# Create a SQLDatabase using the data
db = SQLDatabase.from_uri("postgresql://postgres:@localhost:5432/postgres")

# Creating a SQLDatabaseToolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Creating a chat agent
agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)


st.set_page_config(page_title="NDM Agents", page_icon="🧠")
st.title("🧠NDM Agents")

option = st.selectbox(
    'Langchain Module Option:',
    ('create_sql_agent', 'SQLDatabaseChain'))


db_chain = SQLDatabaseChain.from_llm(ChatOpenAI(temperature=0, deployment_id="gpt-35-turbo-0613")
                                     , db
                                     , verbose=True
                                     , use_query_checker=True)




if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with  st.chat_message("assistent"):
        st.write("🧠 thinking ...")
        st_callback = StreamlitCallbackHandler(st.container())
        if option == "create_sql_agent":
            response = agent.run(prompt, callbacks=[st_callback])
        elif option == "SQLDatabaseChain":
            response = db_chain.run(prompt, callbacks=[st_callback])
        st.write(response)


