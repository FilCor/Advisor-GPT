import boto3
from botocore.exceptions import ClientError
import botocore.config

def get_aws_parameter(param_name, decrypt=False):
    """Ottieni un parametro da AWS Systems Manager Parameter Store."""
    config = botocore.config.Config(region_name='eu-north-1')  # Usa solo il codice della regione
    ssm = boto3.client('ssm', config=config)
    try:
        parameter = ssm.get_parameter(Name=param_name, WithDecryption=decrypt)
        return parameter['Parameter']['Value']
    except ClientError as e:
        print(f"Errore nel recupero del parametro {param_name}: {e}")
        return None
