import asyncio
import logging.config
from functools import wraps
from urllib.parse import urljoin

import boto3
import typer
from rich import print as rprint

from confluence_chat.attlasian.confluence import confluence_client
from confluence_chat.conf.logging import logging_config
from confluence_chat.conf.settings import settings
from confluence_chat.services.aws import bedrock_agent_client

logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

app = typer.Typer()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@app.command()
@coro  # type: ignore[misc]
async def main(key: list[str] | None = None) -> None:
    """
    :key list[str]: A Confluence workspace key

    Loads Confluence data into S3 bucket
    to adjust Bedrock knowledge base.
    """

    s3_client = boto3.client("s3")

    spaces = await confluence_client.get_spaces(keys=key)
    if not spaces:
        logger.error("No spaces found")
        exit(1)

    uploaded_pages = 0

    for space in spaces:
        rprint(f'[yellow]Processing space "{space.name}".[/yellow]')
        pages = await confluence_client.get_pages(space_id=space.id)

        for page in pages:
            typer.echo(f"Processing page {page.title}")
            author = await confluence_client.get_user(account_id=page.authorId)

            content = page.body.storage.value.replace("&quot", "")
            source = urljoin(str(settings.confluence.host), page.links.webui)

            body = (
                f"Original Confluence source: {source}\n"
                f"Document metadata:\n{page.model_dump_json(exclude={"body"})}\n"
                f"Author info:\n{author}\n"
                f"HTML body:```html\n{content}```"
            )

            typer.echo("Upload page content to S3 bucket.")
            s3_client.put_object(
                Bucket=settings.aws.s3_bucket,
                Key=f"docs/{page.title}.txt",
                Body=body.encode("utf-8"),
            )
            uploaded_pages += 1

    # Ingestion job to sync new files with the data store
    bedrock_agent_client.start_ingestion_job(
        knowledgeBaseId=settings.aws.knowledge_base_id,
        dataSourceId=settings.aws.data_source_id,
    )

    rprint("[blue]Ingestion job started.[/blue]")
    rprint(f"[green]{uploaded_pages} pages successfully uploaded.[/green]")


if __name__ == "__main__":
    asyncio.run(app())
