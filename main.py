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


instance_id = 'i-022949ac44260fcb1'
hostedzone_id = 'Z0919409KSY4PU0EQGIP'


ec2 = boto3.client('ec2')
#response = ec2.describe_instances()

# Get allocation id
filters = [
    {'Name': 'domain', 'Values': ['vpc']}
]
response = ec2.describe_addresses(Filters=filters)

for addr in response['Addresses']:
    if addr['InstanceId'] == instance_id:
        allocation_id = addr['AllocationId']
print('allocation id:')
print(allocation_id)

# Release eip
try:
    response = ec2.release_address(AllocationId=allocation_id)
except ClientError as e:
    print(e)
print('eip released')

#allocation new ip
try:
    allocation = ec2.allocate_address(Domain='vpc')
    response = ec2.associate_address(AllocationId=allocation['AllocationId'],
                                     InstanceId=instance_id)
except ClientError as e:
    print(e)
print('new ip allocated')


#get new ip
response = ec2.describe_addresses(Filters=filters)
for addr in response['Addresses']:
    if addr['InstanceId'] == instance_id:
        pub_ip = addr['PublicIp']
print('new ip:')
print(pub_ip)

#update DNS record
route53 = boto3.client('route53')
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


js = json.dumps(response, sort_keys=True, indent=4, cls=ComplexEncoder)
print(js)
