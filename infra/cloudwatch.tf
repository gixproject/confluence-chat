resource "aws_cloudwatch_log_group" "default_log_group" {
  name = "${local.project_name}-${var.environment}"
}

resource "aws_cloudwatch_log_stream" "backend_logstream" {
  name           = "app"
  log_group_name = aws_cloudwatch_log_group.default_log_group.name
}

resource "aws_cloudwatch_log_stream" "nginx_logstream" {
  name           = "nginx"
  log_group_name = aws_cloudwatch_log_group.default_log_group.name
}
