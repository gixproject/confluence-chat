import boto3

from confluence_chat.conf.settings import settings

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=settings.aws.region,
)

bedrock_agent_client = boto3.client(
    service_name="bedrock-agent",
    region_name=settings.aws.region,
)
