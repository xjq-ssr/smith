import aws
import os

instance_id = 'i-0e01cf02fba13bba5'
hostedzone_id = 'Z0919409KSY4PU0EQGIP'

clear_command = "rd /s/q C:\\Users\\xjq\\AppData\\Local\\Google\\Chrome"
print os.system(clear_command)
print 'Create new Chrome environment ... done'

print 'Get new IP address ...'
new_ip = aws.change_eip(instance_id,hostedzone_id)
print 'Your current IP is ' + new_ip

create_command = "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 1 /f"
change_command = "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\" /v ProxyServer /d \"" + new_ip + ":10086\" /f"

print os.system(create_command)
print os.system(change_command)

print 'NOTICE! You will loose this IP forever after logout'


