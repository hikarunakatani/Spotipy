import * as cdk from "aws-cdk-lib";
import { AssetCode, Runtime, LayerVersion, Code } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import { Function } from "aws-cdk-lib/aws-lambda";
import { Rule, Schedule } from "aws-cdk-lib/aws-events";
import { LambdaFunction } from "aws-cdk-lib/aws-events-targets";
import { Topic } from "aws-cdk-lib/aws-sns";
import { EmailSubscription } from "aws-cdk-lib/aws-sns-subscriptions";
import * as apigw from 'aws-cdk-lib/aws-apigateway';
import * as iam from "aws-cdk-lib/aws-iam";
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import secretValue from '../secret.json'
export class SpotipyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define a topic for lambda
    const topic = new Topic(this, "Topic", {
      displayName: "Topic to send email from lambda",
    });

    topic.addSubscription(new EmailSubscription("hikamichael@hotmail.co.jp"));


    
    const secret = new secretsmanager.Secret(this, 'spotipy-secret', {
      generateSecretString: {
        secretStringTemplate: JSON.stringify(secretValue),
        generateStringKey: 'password',
      },
    });

    // Define a role for lambda
    const lambdaRole = new iam.Role(this, "lambdaRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });

    // Grant lambda to get secrets values from secrets manager
    lambdaRole.addToPolicy(
      new iam.PolicyStatement({
        resources: ["*"],
        actions: ["secretsmanager:GetSecretValue", "sns:Publish"],
      })
    );

    // Define a lambda layer
    const lambdaLayer = new LayerVersion(this, "LambdaLayer", {
      code: AssetCode.fromAsset("lambda_layer"),
      compatibleRuntimes: [Runtime.PYTHON_3_9],
    });

    // Define a lambda Function
    const lambda = new Function(this, "Spotipy", {
      functionName: "Spotipy",
      runtime: Runtime.PYTHON_3_9,
      code: Code.fromAsset("lambda"),
      handler: "invoke.handler",
      layers: [lambdaLayer],
      role: lambdaRole,
      timeout: cdk.Duration.minutes(15),
      environment: {
        TOPIC_ARN: topic.topicArn,
        SECRET_ARN: secret.secretArn,
      },
    });

    // defines an API Gateway REST API resource backed by lambda function.
    const apigateway =  new apigw.LambdaRestApi(this, 'Endpoint', {
      handler: lambda
    });

    // Define an EventBridge rule
    const rule = new Rule(this, "RuleToInvokeLambda", {
      schedule: Schedule.cron({
        minute: "0",
        hour: "0",
        month: "*",
        year: "*",
        weekDay: "L",
      }),
      targets: [new LambdaFunction(lambda)],
    });

  }
}
