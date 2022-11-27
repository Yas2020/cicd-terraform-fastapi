
resource "aws_db_parameter_group" "fastapi-db" {
  name   = "fastapi-db"
  family = "postgres13"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}


# ---------------------------------------------------------------------------------------------------------------------
# RDS DB SUBNET GROUP
# ---------------------------------------------------------------------------------------------------------------------
resource "aws_db_subnet_group" "db-subnet-grp" {
  name        = "fastapi-db-sgrp"
  description = "Database Subnet Group"
  subnet_ids  = aws_subnet.private.*.id
}

# ---------------------------------------------------------------------------------------------------------------------
# RDS (MYSQL)
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_db_instance" "db" {
  identifier             = "fastapi"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "13.3"
  port                   = "5432"
  instance_class         = var.db_instance_type
  db_name                = var.db_name
  username               = var.db_user
  password               = data.aws_ssm_parameter.dbpassword.value
  availability_zone      = "${var.aws_region}a"
  vpc_security_group_ids = [aws_security_group.db-sg.id]
  multi_az               = false
  db_subnet_group_name   = aws_db_subnet_group.db-subnet-grp.id
  parameter_group_name   = aws_db_parameter_group.fastapi-db.name
  publicly_accessible    = false
  skip_final_snapshot    = true

  tags = {
    Name = "${var.stack}-db"
  }
}

output "db_host" {
  value = aws_db_instance.db.address
}

output "db_port" {
  value = aws_db_instance.db.port
}

output "db_url" {
  value = "postgresql://${aws_db_instance.db.address}/${var.db_name}"
}