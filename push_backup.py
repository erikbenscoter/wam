import os
import datetime



def getDateFolderName():
	date_string = datetime.datetime.today()
	date_string = str(date_string).replace(" ","_")
	date_string = date_string.split(".")[0]
	return date_string


def getBackupPath():
	date_string = getDateFolderName()
	path = "/freeAgent/ruth_data_backup/{}".format(date_string)
	return path

def makeFolder():
	backup_path = getBackupPath()
	cmd = "mkdir -p {}/fixtures/".format(backup_path)
	os.system(cmd)

def copyJsonFiles():
	cmd = "cp ./fixtures/* {}/fixtures/".format(str(getBackupPath()))
	os.system(cmd)

makeFolder()
copyJsonFiles()
