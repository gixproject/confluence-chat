import logging

from langchain_aws import ChatBedrock

from confluence_chat.conf.settings import settings
from confluence_chat.services.aws import bedrock_client

logger = logging.getLogger(__name__)

chat_model = ChatBedrock(
    client=bedrock_client,
    model_id=settings.aws.bedrock_chat_model,  # type: ignore[call-arg]
    temperature=settings.aws.model_temperature,
    guardrails={
        "guardrailIdentifier": settings.aws.bedrock_guardrial_id,
        "guardrailVersion": "1",
        "trace": True,
    },
)
