import boto3
from botocore.exceptions import ClientError

def get_aws_parameter(param_name, decrypt=False):
    """Ottieni un parametro dal AWS Parameter Store."""
    ssm = boto3.client('ssm')
    try:
        parameter = ssm.get_parameter(Name=param_name, WithDecryption=decrypt)
        return parameter['Parameter']['Value']
    except ClientError as e:
        print(f"Errore nel recupero del parametro {param_name}: {e}")
        return None
