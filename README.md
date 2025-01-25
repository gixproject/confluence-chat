[![Build](https://github.com/gixproject/confluence-chat/actions/workflows/default.yaml/badge.svg)](https://github.com/gixproject/confluence-chat/actions/workflows/default.yaml)
[![Terraform sources](https://github.com/gixproject/confluence-chat/actions/workflows/infra.yaml/badge.svg)](https://github.com/gixproject/confluence-chat/actions/workflows/infra.yaml)
[![Staging deploy](https://github.com/gixproject/confluence-chat/actions/workflows/deploy_staging.yaml/badge.svg)](https://github.com/gixproject/confluence-chat/actions/workflows/deploy_staging.yaml)

# Confluence-chat

## Description

Confluence chat allows you to connect and chat with your confluence using Bedrock knowdledge base.

## Usage

### AWS credentials

To use the AWS resources you need to configure
your [AWS credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).
To use your existing local AWS profile (**but not default**) credentials set the `AWS_PROFILE` env variable.

### Local development

1. Run setup script to install the app dependencies.

```bash
./local_setup.sh
```

2. Fill the `.env` with the valid environment variables values.
3. Run the app:

```bash
poetry run streamlit run confluence_chat/app.py --server.runOnSave=true
```

### Docker deployment

You can run the application will be available on `80` port (http://localhost).

```bash
docker compose --profile server build
docker compose --profile server up
```

### Authentication credentials
To log in into application use the following credentials:

```bash
username: j_smith
password: 0af3!192Dm5^
```

You may change or adjust credentials in the `.streamlit/credentials.yaml` file.

## Useful

### Makefile

It may be easy to develop/test the application using shortcuts.

```bash
make app
make load_data
```

### Load data to chat

To load Confluence data into Amazon Bedrock knowledge base.

```bash
poetry run python confluence_chat/commands/load_data.py --key={space_key}
```

### Git hooks

To check the code before every commit you may install Git hooks.
All hooks would be installed automatically while running `./local_setup.sh`.

```bash
pre-commit install
```
