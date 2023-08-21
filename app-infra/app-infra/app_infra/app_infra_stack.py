from aws_cdk import (
    # Duration,
    Stack, StackProps
    
)
from constructs import Construct
import aws_cdk.aws_lambda as lambda_


class AppInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        apiLambda = lambda_.Function(self, "llm",
                                     runtime=lambda_.Runtime.PYTHON_3_11,
                                     code= lambda_.Code.from_asset("../app/"),
                                     handler="unias_api.handler",

        )

        