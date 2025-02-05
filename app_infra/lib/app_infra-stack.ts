import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apiGateway from 'aws-cdk-lib/aws-apigateway'
import * as dotenv from "dotenv";

dotenv.config()

export class AppInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const layer = new lambda.LayerVersion(this, 'BaseLayer', {
        code: lambda.Code.fromAsset('lambda_base_layer/layer.zip'),
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_11]
    });

    const apiLambda = new lambda.Function(this,'ApiFunction', {
        runtime: lambda.Runtime.PYTHON_3_11,
        code: lambda.Code.fromAsset('../app_scratch/'),
        handler: 'unias_scratch_api.handler',
        layers: [layer],
        environment:{
            "GOOGLE_API_KEY": process.env.GOOGLE_API_KEY ?? '',
            "QDRANT_HOST": process.env.QDRANT_HOST ?? '',
            "QDRANT_API_KEY": process.env.QDRANT_API_KEY ?? '',

        }
    });

    const uniasApi = new apiGateway.RestApi(this, 'RestApi',{
        restApiName:'UniasAPI'
    });

    uniasApi.root.addProxy({
        defaultIntegration:  new apiGateway.LambdaIntegration(apiLambda),

    });
    }

}



//update the lambda layer one time, then update the nextJS, and we will have a working knowledge base.