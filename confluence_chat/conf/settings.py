from pydantic import Field, EmailStr, HttpUrl
from pydantic_settings import BaseSettings as _BaseSettings


class BaseSettings(
    _BaseSettings,
    env_file=".env",
    extra="ignore",
):
    pass


class AWSSettings(BaseSettings, env_prefix="aws_"):
    region: str
    s3_bucket: str
    bedrock_chat_model: str
    bedrock_guardrial_id: str
    knowledge_base_id: str
    data_source_id: str
    model_temperature: float = 0.0

    @property
    def model_kwargs(self):
        return {
            "max_tokens": 2048,
            "temperature": 0.0,
            "top_k": 250,
            "top_p": 1,
            "stop_sequences": ["\n\nHuman"],
        }


class ConfluenceSettings(BaseSettings, env_prefix="confluence_"):
    email: EmailStr
    host: HttpUrl
    token: str


class Settings(BaseSettings):
    aws: AWSSettings = Field(default_factory=AWSSettings)  # type: ignore[arg-type]
    confluence: ConfluenceSettings = Field(default_factory=ConfluenceSettings)  # type: ignore[arg-type]

    debug: bool = False


settings = Settings()
