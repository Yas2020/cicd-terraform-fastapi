resource "aws_ecs_cluster" "ecs-cluster" {
  name = "${var.stack}-Cluster"
}


resource "aws_ecs_task_definition" "task-def" {
  family                   = var.family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.tasks-service-role.arn

  container_definitions = <<DEFINITION
[
  {
    "cpu": ${var.fargate_cpu},
    "image": "${aws_ecr_repository.image_repo.repository_url}",
    "memory": ${var.fargate_memory},
    "name": "${var.family}",
    "networkMode": "awsvpc",
    "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "${var.cw_log_group}",
                "awslogs-region": "${var.aws_region}",
                "awslogs-stream-prefix": "${var.cw_log_stream}"
            }
        },
    "environment": [
            {
                "name": "DATABASE_HOSTNAME",
                "value": "${aws_db_instance.db.address}"
            },
            {
                "name": "DATABASE_USERNAME",
                "value": "${var.db_user}"
            },
            {
                "name": "DATABASE_PASSWORD",
                "value": "${data.aws_ssm_parameter.dbpassword.value}"
            },
            {
                "name": "DATABASE_NAME",
                "value": "${var.database_name}"
            },
            {
                "name": "DATABASE_PORT",
                "value": "${var.database_port}"
            },
            {
                "name": "SECRET_KEY",
                "value": "${var.secret_key}"
            },
            {
                "name": "ALGORITHM",
                "value": "${var.algorithm}"
            },
            {
                "name": "ACCESS_TOKEN_EXPIRE_MINUTES",
                "value": "${var.minutes}"
            },
            {
                "name": "fastapi.datasource.initialize",
                "value": "${var.db_initialize}"
            },
            {
                "name": "fastapi.profiles.active",
                "value": "${var.db_profile}"
            },
            {
                "name": "fastapi.datasource.url",
                "value": "postgresql://${aws_db_instance.db.address}/${var.db_name}"
            }
        ],
    "portMappings": [
      {
        "containerPort": ${var.container_port},
        "hostPort": ${var.container_port}
      }
    ]
  }
]
DEFINITION
}

# ---------------------------------------------------------------------------------------------------------------------
# ECS SERVICE
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_ecs_service" "service" {
  name            = "${var.stack}-Service"
  cluster         = aws_ecs_cluster.ecs-cluster.id
  task_definition = aws_ecs_task_definition.task-def.arn
  desired_count   = var.task_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.task-sg.id]
    subnets         = aws_subnet.private.*.id
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.trgp.id
    container_name   = var.family
    container_port   = var.container_port
  }

  depends_on = [
    aws_alb_listener.alb-listener,
  ]
}

# ---------------------------------------------------------------------------------------------------------------------
# CLOUDWATCH LOG GROUP
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "fastapi-cw-lgrp" {
  name = var.cw_log_group
}