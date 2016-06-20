from django.shortcuts import render,redirect
import os

# Create your views here.
class DBManager:
    def dumpData(request):
        os.system("echo $PWD")
        
        cmd = "sh dump_the_data.sh"
        os.system(cmd)
        return redirect("/")
