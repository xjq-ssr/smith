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
route53 = boto3.client('route53')

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


def change_eip(instance_id, hostedzone_id):

    filters = [
        {'Name': 'domain', 'Values': ['vpc']}
    ]
    response = ec2.describe_addresses(Filters=filters)
    for addr in response['Addresses']:
        if addr['InstanceId'] == instance_id:
            allocation_id = addr['AllocationId']

    try:
        response = ec2.release_address(AllocationId=allocation_id)
    except ClientError as e:
        pass

    try:
        allocation = ec2.allocate_address(Domain='vpc')
        response = ec2.associate_address(AllocationId=allocation['AllocationId'],
                                        InstanceId=instance_id)
    except ClientError as e:
        pass

    response = ec2.describe_addresses(Filters=filters)
    for addr in response['Addresses']:
        if addr['InstanceId'] == instance_id:
            pub_ip = addr['PublicIp']
    
    response = route53.change_resource_record_sets(
        HostedZoneId = hostedzone_id,
        ChangeBatch={
            'Comment': 'update dns record',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'ssr.xjqpro.com',
                        'Type': 'A',
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': pub_ip,
                            },
                        ]
                    }
                },
            ]
        }
    )  

    return pub_ip