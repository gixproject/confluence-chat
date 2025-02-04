resource "aws_iam_role" "ec2_role" {
  name               = "${local.project_name}${var.environment}EC2AccessRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_iam_policy" "ec2_role_policy" {
  name   = "${local.project_name}${var.environment}EC2Default"
  policy = data.aws_iam_policy_document.ec2_default_policy.json
}

resource "aws_iam_role_policy_attachment" "ec2_policy_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.ec2_role_policy.arn
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${local.project_name}${var.environment}Default"
  role = aws_iam_role.ec2_role.name
}

resource "aws_instance" "server" {
  ami                         = "ami-05576a079321f21f8" # Amazon Linux 2023
  instance_type               = "t2.micro"
  key_name                    = "${local.project_name}-keypair"
  vpc_security_group_ids      = [aws_security_group.main_security_group.id]
  subnet_id                   = aws_subnet.main_subnet.id
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name

  root_block_device {
    volume_type = "gp2"
    volume_size = 30
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }

  user_data_base64            = base64encode(local.user_data)
  user_data_replace_on_change = true

  provisioner "file" {
    source      = var.project_source
    destination = "/home/ec2-user/${local.project_name}"
  }

  provisioner "remote-exec" {
    inline = [
      "echo 'Waiting for user data script to finish'",
      "cloud-init status --wait > /dev/null",
      "cd ${local.project_name}",
      "sudo chmod 666 /var/run/docker.sock",
      "sudo chmod +x ./infra/service_start.sh",
      "./infra/service_start.sh",
      "echo 'Loading sample data'",
    ]
  }

  tags = {
    Name = "${local.project_name}-${var.environment}-app"
  }
}
