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
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
from urllib.parse import quote_plus
import streamlit as st


st.set_page_config(page_title="NDM Agent V2", page_icon="📅")
st.title("📅 NDM Agent V2")

db = SQLDatabase.from_uri(f'postgresql://{os.getenv("DB_USER_NDM")}:{os.getenv("DB_PASS_NBOT")}@10.54.68.243:3254/db_nasional', 
                            schema="nation_bot",
                          include_tables=["rev_rpmb_siteid_monthly_nation","revenue_siteid_day","payload_traffic_vlr_daily","transport_site_performance_4g_week"],
                          sample_rows_in_table_info=3,
                          )




toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0, deployment_id="gpt-35-turbo-0613"))

db_chain = SQLDatabaseChain.from_llm(ChatOpenAI(temperature=0, deployment_id="gpt-35-turbo-0613")
                                     , db
                                     , verbose=True
                                     , use_query_checker=True)

agent = create_sql_agent(
    ChatOpenAI(temperature=0, deployment_id="gpt-35-turbo-0613"),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with  st.chat_message("assistent"):
        st.write("🧠 thinking ...")
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)
