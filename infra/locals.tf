locals {

  main_bucket_name = "confluence-chat"
  project_name     = "confluence-chat"
  stack_name       = "confluence-chat"

  user_data = <<-EOT
                #!/bin/bash
                set -ef -o pipefail
                sudo yum update -y
                DOCKER_CONFIG=/home/ec2-user/.docker
                sudo yum install -y git docker
                sudo usermod -a -G docker ec2-user
                mkdir -p $DOCKER_CONFIG/cli-plugins
                curl -SL https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
                sudo chown ec2-user -R $DOCKER_CONFIG
                sudo chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
                sudo systemctl start docker.service
                sudo systemctl enable docker.service

                # Put environment variables to .env file
                cd /home/ec2-user/${local.project_name}
                printf "%s\n" \
                 "LOG_LEVEL=INFO" \
                 "CONFLUENCE_EMAIL=${var.confluence_email}" \
                 "CONFLUENCE_TOKEN=${var.confluence_token}" \
                 "CONFLUENCE_HOST=${var.confluence_host}" \
                 "AWS_S3_BUCKET=${local.main_bucket_name}" \
                 "AWS_BEDROCK_GUARDRIAL_ID=6onin5akxvy1 \
                 "AWS_KNOWLEDGE_BASE_ID=TCXBA8ZJW7 \
                 "AWS_DATA_SOURCE_ID=VBFFP8FBWA \
                 "AWS_REGION=${var.region}" \
                 "LOG_DRIVER=awslogs" \
                 "AWS_LOG_GROUP=${local.project_name}-${var.environment}" \
                 "AWS_BEDROCK_CHAT_MODEL=us.anthropic.claude-3-5-sonnet-20241022-v2:0" >> .env
                EOT
}
