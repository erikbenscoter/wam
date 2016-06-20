from VacationScheduler.settings import INSTALLED_APPS
import os

for app in INSTALLED_APPS:
    clean_app = app.split(".")[-1]
    cmd = "python3 manage.py dumpdata {} --indent=4 > ./fixtures/{}.json".format(str(clean_app),str(clean_app))
    os.system(cmd)
