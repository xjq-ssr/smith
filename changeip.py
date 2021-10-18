import aws

instance_id = 'i-022949ac44260fcb1'
hostedzone_id = 'Z0919409KSY4PU0EQGIP'

print(aws.change_eip(instance_id,hostedzone_id))