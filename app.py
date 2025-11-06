#!/usr/bin/env python3
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_iam as iam,
    CfnOutput,
    Duration,
)
from constructs import Construct

class ProductionStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # VPC with high availability
        vpc = ec2.Vpc(
            self, "ProductionVPC",
            max_azs=3,
            nat_gateways=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Isolated",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )
        
        # Security Group
        security_group = ec2.SecurityGroup(
            self, "SecurityGroup",
            vpc=vpc,
            description="Production security group",
            allow_all_outbound=True
        )
        
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow HTTPS"
        )
        
        # CloudWatch Log Group
        log_group = logs.LogGroup(
            self, "LogGroup",
            retention=logs.RetentionDays.ONE_MONTH
        )
        
        # Outputs
        CfnOutput(self, "VpcId", value=vpc.vpc_id, description="VPC ID")
        CfnOutput(self, "SecurityGroupId", value=security_group.security_group_id)
        CfnOutput(self, "LogGroupName", value=log_group.log_group_name)
