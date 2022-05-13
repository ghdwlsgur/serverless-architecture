import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
  response = sns.publish(
    TopicArn = 'SNS ARN 붙여넣기'
    Message = event.['Records'][0]['s3']['object']['key'] + ' has been ' + event['Records'][0]['eventName'],
    Subject = 'S3 Event',
  )

  return {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
  }