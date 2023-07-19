resource "aws_db_instance" "unsafe_rds_db" {
  cluster_identifier  = aws_rds_cluster.default.id
  publicly_accessible = true
}

resource "aws_rds_cluster_instance" "unsafe_cluster" {
  cluster_identifier  = aws_rds_cluster.default.id
  publicly_accessible = true
}

resource "aws_rds_cluster_instance" "safe_cluster" {
  cluster_identifier  = "aurora-cluster-demo"
  publicly_accessible = false
}
