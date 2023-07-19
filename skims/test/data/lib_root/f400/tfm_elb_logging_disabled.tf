resource "aws_elb" "unsafe_elb" {
  name = "foobar-terraform-elb"

  access_logs {
    bucket  = "foo"
    enabled = false
  }

}

resource "aws_lb" "unsafe_elbv2" {
  name = "foobar-terraform-elb"

  access_logs {
    bucket  = "foo"
    enabled = false
  }

}

resource "aws_lb" "safe_elbv2" {
  name = "foobar-terraform-elb"

  access_logs {
    bucket  = "foo"
    enabled = true
  }

}