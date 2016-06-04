import os

def setUpToRunHourly():
    cmd = "sudo echo '#!/bin/bash \n firefox http://www.blah93.tk/update\n sh /home/erikbenscoter/projects/wam/dump_the_data.sh' > /etc/cron.hourly/wam_update"
    os.system(cmd)
    cmd = "sudo chmod 755 /etc/cron.hourly/wam_update"
    os.system(cmd)
