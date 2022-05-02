import aws
import os

instance_id = 'i-0e01cf02fba13bba5'
hostedzone_id = 'Z0919409KSY4PU0EQGIP'

a = os.system('rd /s/q C:\\Users\\xjq\\AppData\\Local\\Google\\Chrome')
print a
print 'Create new Chrome environment ... done'

print 'Get new IP address ...'
new_ip = aws.change_eip(instance_id,hostedzone_id)
print 'Your current IP is ' + new_ip

print 'NOTICE! You will loose this IP forever after logout'

