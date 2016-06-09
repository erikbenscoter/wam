from VacationScheduler.settings import INSTALLED_APPS
import os

for app in INSTALLED_APPS:
    if(not len(app.split(".")) > 1):
        cmd = "python3 manage.py dumpdata {} --indent=4 > ./fixtures/{}.json".format(str(app),str(app))
        os.system(cmd)
