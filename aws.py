import boto3
import json
from datetime import date, datetime
from botocore.exceptions import ClientError


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


ec2 = boto3.client('ec2')


def get_eip(instance_id):

    filters = [
        {'Name': 'domain', 'Values': ['vpc']}
    ] 
    
    try:
        response = ec2.describe_addresses(Filters=filters)
        for addr in response['Addresses']:
            if addr['InstanceId'] == instance_id:
                pub_ip = addr['PublicIp']
        return pub_ip
    except Exception as e:
        print(e)
