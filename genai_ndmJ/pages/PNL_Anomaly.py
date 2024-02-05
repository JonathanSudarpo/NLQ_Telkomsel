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


st.set_page_config(page_title="PLN Anomaly", page_icon="⚡")
st.title("⚡PLN Anomaly")

custom_table_info = {
    "output_anomali_detection_pln": """CREATE TABLE `output_anomali_detection_pln` (
  `date` datetime DEFAULT NULL,
  `yearmonth` bigint(20) DEFAULT NULL,
  `year` bigint(20) DEFAULT NULL,
  `month` bigint(20) DEFAULT NULL,
  `idpel` bigint(20) DEFAULT NULL,
  `site_id` text DEFAULT NULL,
  `nama_pelanggan` text DEFAULT NULL,
  `golongan_tarif` text DEFAULT NULL,
  `regional` text DEFAULT NULL,
  `status` text DEFAULT NULL,
  `bill_type` text DEFAULT NULL,
  `daya` bigint(20) DEFAULT NULL,
  `kwh_awal` bigint(20) DEFAULT NULL,
  `kwh_akhir` bigint(20) DEFAULT NULL,
  `kwh_pakai` bigint(20) DEFAULT NULL,
  `rptag` bigint(20) DEFAULT NULL,
  `tagihan` bigint(20) DEFAULT NULL,
  `rptag_ideal` double DEFAULT NULL,
  `denda_percent` double DEFAULT NULL,
  `site_utility` text DEFAULT NULL,
  `lte_bandwidth` double DEFAULT NULL,
  `band_lte` text DEFAULT NULL,
  `payload_total_mbyte_sum_monthly` double DEFAULT NULL,
  `outlier_fine_payment_upper` bigint(20) DEFAULT NULL,
  `outlier_fine_payment_lower` bigint(20) DEFAULT NULL,
  `outlier_total_payment_upper` bigint(20) DEFAULT NULL,
  `outlier_total_payment_lower` bigint(20) DEFAULT NULL,
  `outlier_kwh_group_upper` bigint(20) DEFAULT NULL,
  `outlier_kwh_group_lower` bigint(20) DEFAULT NULL,
  `outlier_daya_group_upper` bigint(20) DEFAULT NULL,
  `outlier_daya_group_lower` bigint(20) DEFAULT NULL,
  `outlier_siteutil_group_upper` bigint(20) DEFAULT NULL,
  `outlier_siteutil_group_lower` bigint(20) DEFAULT NULL,
  `outlier_bwgroup_group_upper` bigint(20) DEFAULT NULL,
  `outlier_bwgroup_group_lower` bigint(20) DEFAULT NULL,
  `outlier_payloadgroup_group_upper` bigint(20) DEFAULT NULL,
  `outlier_payloadgroup_group_lower` bigint(20) DEFAULT NULL,
  `outlier_pln_lebih_dari_0_kwh_0` bigint(20) DEFAULT NULL,
  `outlier_pln0_kwh_lebih_dari_0` bigint(20) DEFAULT NULL,
  `final_score` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
)

/*
3 rows from output_anomali_detection_pln table:
date	yearmonth	year	month	idpel	site_id	nama_pelanggan	golongan_tarif	regional	status	bill_type	daya	kwh_awal	kwh_akhir	kwh_pakai	rptag	tagihan	rptag_ideal	denda_percent	site_utility	lte_bandwidth	band_lte	payload_total_mbyte_sum_monthly	outlier_fine_payment_upper	outlier_fine_payment_lower	outlier_total_payment_upper	outlier_total_payment_lower	outlier_kwh_group_upper	outlier_kwh_group_lower	outlier_daya_group_upper	outlier_daya_group_lower	outlier_siteutil_group_upper	outlier_siteutil_group_lower	outlier_bwgroup_group_upper	outlier_bwgroup_group_lower	outlier_payloadgroup_group_upper	outlier_payloadgroup_group_lower	outlier_pln_lebih_dari_0_kwh_0	outlier_pln0_kwh_lebih_dari_0	final_score
5/1/2023 0:00	202305	2023	5	110000171558	MBO042	DMT_TSEL_MBO042_RSUDMBO   	P3	R01 - SUMBAGUT	Active	postpaid	7700	93053	94070	1017	1616186	1616186	1469259.9	10.00000749	End Site	60	{LTE1800}	9626076.173	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
5/1/2023 0:00	202305	2023	5	110000190967	MBO063	TELKOMSEL-MBO063-A	R1T	R01 - SUMBAGUT	Active	postpaid	33000	18826	22964	4138	6585986	6585986	5978168.6	10.16728434	Simpul	70	{LTE2100,LTE900}	39276953.3	0	0	0	0	0	0	0	0	0	0	1	0	1	0	0	0	0.333333333
5/1/2023 0:00	202305	2023	5	110000198241	MBO901	TELKOMSEL-MBO901-A	Â  B2	R01 - SUMBAGUT	Active	postpaid	23000	233309	235742	2433	3866451	3866451	3514955.1	10.0000111	End Site	60	{LTE1800}	21297451.58	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
*/"""}


db = SQLDatabase.from_uri(f'mysql+pymysql://{os.getenv("DB_USER_101")}:%s@10.54.68.101:3306/summary' % quote_plus(os.getenv("DB_PASS_101")), 
                          include_tables=["output_anomali_detection_pln"],
                          custom_table_info = custom_table_info,
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
