output "public_ip" {
  value = "http://${aws_eip.server_eip.public_ip}"
}

output "public_dns" {
  value = "http://${aws_eip.server_eip.public_dns}"
}
