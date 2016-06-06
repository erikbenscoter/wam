from VacationScheduler.settings import INSTALLED_APPS

for app in INSTALLED_APPS:
    cmd = "python3 manage.py dumpdata {} --indent=4 > ./fixtures/{}.json".format(str(app),str(app))
    os.system(cmd)
