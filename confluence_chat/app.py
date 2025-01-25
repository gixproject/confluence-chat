import logging.config
import time
from operator import itemgetter

import streamlit as st
import yaml
from langchain_aws import AmazonKnowledgeBasesRetriever
from langchain_aws.retrievers.bedrock import RetrievalConfig, VectorSearchConfig
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableParallel
from streamlit_authenticator import Authenticate
from yaml import SafeLoader

from confluence_chat.conf.logging import logging_config
from confluence_chat.conf.settings import settings
from confluence_chat.llm.prompts import INITIAL_PROMPT
from confluence_chat.common.constants import BOT_DESCRIPTION
from confluence_chat.llm.models import chat_model

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Confluence Chat",
    page_icon="🤖",
)

# -------------------- Base auth --------------------

with open(".streamlit/credentials.yaml") as file:
    credentials = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    credentials["credentials"],
    credentials["cookie"]["name"],
    credentials["cookie"]["key"],
    credentials["cookie"]["expire_days"],
)

try:
    authenticator.login(location="main")
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout(location="sidebar")
    st.write(f'Welcome, *{st.session_state["name"]}*')
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
    st.stop()
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
    st.stop()


# -------------------- Init resources --------------------


@st.cache_resource
def get_llm_model() -> BaseChatModel:
    return chat_model


llm = get_llm_model()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", INITIAL_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ],
)

# Initialize langchain chain with history
history = StreamlitChatMessageHistory(key="chat_messages")

retriever = AmazonKnowledgeBasesRetriever(  # type: ignore[call-arg]
    knowledge_base_id=settings.aws.knowledge_base_id,
    retrieval_config=RetrievalConfig(vectorSearchConfiguration=VectorSearchConfig(numberOfResults=20)),
    region_name=settings.aws.region,
)

chain = (
    RunnableParallel(
        {  # type: ignore[arg-type]
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "history": itemgetter("history"),
        },
    )
    .assign(response=prompt | llm | StrOutputParser())
    .pick(["response", "context"])
)

history_chain = RunnableWithMessageHistory(
    chain,  # type: ignore[arg-type]
    lambda session_id: history,
    input_messages_key="question",
    history_messages_key="history",
)


def clear_chat_history():
    history.messages.clear()


# -------------------- Streamlit --------------------

st.header("Hello in the Confluence chat 👋")
st.write(BOT_DESCRIPTION)

with st.sidebar:
    st.button("+ New chat", on_click=clear_chat_history, type="secondary")
    st.divider()

# Display first message from AI
if not history.messages:
    history.add_ai_message("How may I assist you today?")

# Render current messages from StreamlitChatMessageHistory
for msg in history.messages:
    st.chat_message(msg.type).write(msg.content)

# Chat input handler
if user_input := st.chat_input():
    st.chat_message("human").write(user_input)

    # New messages are saved to history automatically
    config = {"configurable": {"session_id": "any"}}

    # Streaming
    placeholder = st.empty()
    full_response = ""

    start_time = time.time()
    for chunk in history_chain.stream({"question": user_input}, config):  # type:ignore[arg-type]
        full_response += chunk.get("response", "")
        placeholder.chat_message("ai").write(full_response)

    logger.info("LLM invoke time: %s", time.time() - start_time)
    placeholder.chat_message("ai").write(full_response)
    history.add_ai_message(full_response)
