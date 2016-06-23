from django.shortcuts import render,redirect
import os
import push_backup

# Create your views here.
class DBManager:
    def dumpData(request):
        os.system("echo $PWD")

        cmd = "sh dump_the_data.sh"
        os.system(cmd)
        return redirect("/")

    def viewUpdates(request):
        date_folder_name = push_backup.getDateFolderName()
        back_up_path = push_backup.getBackupPath()
        back_up_path = back_up_path.replace(date_folder_name, "")


        all_backups = os.listdir(back_up_path)

        table = []

        for backup in all_backups:
            row = {}
            row["folder"] = str(backup)
            table.append(row)

        context = {
            "table" : table
        }

        
        return render(request,"view_backups/index.html", context)
