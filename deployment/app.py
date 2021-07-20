"""Construct App."""

import os
from typing import Any, Dict, List, Optional

from aws_cdk import aws_apigatewayv2 as apigw
from aws_cdk import aws_apigatewayv2_integrations as apigw_integrations
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda, core
from config import StackSettings

settings = StackSettings()


class titilerLambdaStack(core.Stack):
    """
    Titiler Lambda Stack

    This code is freely adapted from
    - https://github.com/leothomas/titiler/blob/10df64fbbdd342a0762444eceebaac18d8867365/stack/app.py author: @leothomas
    - https://github.com/ciaranevans/titiler/blob/3a4e04cec2bd9b90e6f80decc49dc3229b6ef569/stack/app.py author: @ciaranevans

    """

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        memory: int = 1024,
        timeout: int = 30,
        runtime: aws_lambda.Runtime = aws_lambda.Runtime.PYTHON_3_8,
        concurrent: Optional[int] = None,
        permissions: Optional[List[iam.PolicyStatement]] = None,
        environment: Optional[Dict] = None,
        code_dir: str = "./",
        **kwargs: Any,
    ) -> None:
        """Define stack."""
        super().__init__(scope, id, *kwargs)

        permissions = permissions or []
        environment = environment or {}

        lambda_function = aws_lambda.Function(
            self,
            f"{id}-lambda",
            runtime=runtime,
            code=aws_lambda.Code.from_asset(
                path=os.path.abspath(code_dir),
                bundling=core.BundlingOptions(
                    image=core.BundlingDockerImage.from_asset(
                        os.path.abspath(code_dir),
                        file="Dockerfile",
                    ),
                    command=[
                        "bash",
                        "-c",
                        "cp -R /var/task/. /asset-output/.",
                    ],
                ),
            ),
            handler="handler.handler",
            memory_size=memory,
            reserved_concurrent_executions=concurrent,
            timeout=core.Duration.seconds(timeout),
            environment=environment,
        )

        for perm in permissions:
            lambda_function.add_to_role_policy(perm)

        api = apigw.HttpApi(
            self,
            f"{id}-endpoint",
            default_integration=apigw_integrations.LambdaProxyIntegration(
                handler=lambda_function
            ),
        )
        core.CfnOutput(self, "Endpoint", value=api.url)


app = core.App()

perms = []
if settings.buckets:
    perms.append(
        iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[
                f"arn:aws:s3:::{bucket}/{settings.key}"
                for bucket in settings.buckets
            ],
        )
    )


# Tag infrastructure
for key, value in {
    "Project": settings.name,
    "Stack": settings.stage,
    "Owner": settings.owner,
    "Client": settings.client,
}.items():
    if value:
        core.Tag.add(app, key, value)

lambda_stackname = f"{settings.name}-lambda-{settings.stage}"
titilerLambdaStack(
    app,
    lambda_stackname,
    memory=settings.memory,
    timeout=settings.timeout,
    concurrent=settings.max_concurrent,
    permissions=perms,
    environment=settings.env,
)

app.synth()
