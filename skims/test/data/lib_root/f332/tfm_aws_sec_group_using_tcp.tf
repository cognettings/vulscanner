resource "aws_security_group" "unsafe_group" {
  name = "unsafe_group"

  ingress {
    description = "Ingress rules"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "safe_group" {
  name = "safe_group"

  ingress {
    description = "Ingress rules"
    from_port   = 48000
    to_port     = 48000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
