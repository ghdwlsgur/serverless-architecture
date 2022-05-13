import json
import pymysql
import boto3
import base64
import time
from botocore.exceptions import ClientError

secret_name = "db/practice"
region_name = "ap-northeast-2"

def get_secret():
  session = boto3.session.Session()
  client = session.client(
    service_name = 'secretsmanager',
    region_name = region_name
  )


  get_secret_value_response = client.get_secret_value(
    SecretId = secret_name
  )

  if 'SecretString' in get_secret_value_response:
    secret = get_secret_value_response['SecretString']
    return secret
  else:
    decoded_binary_secret = base64.b63decode(get_secret_value_response['SecretBinary'])
    return decoded_binary_secret

def lambda_handler(event, context):
  secret = get_secret()
  json_secret = json.loads(secret)

  db = pymysql.connect(
    host = 'serverless-app-rds.cimcenmgl8a8.ap-northeast-2.rds.amazonaws.com',
    user = json_secret['username'],
    password = json_secret['password']
  )

  cursor = db.cursor()

  cursor.execute('select now()')
  result = cursor.fetchone()

  db.commit()

  return {
    'statusCode': 200,
    'body': json.dumps(result[0].isoformat())
  }