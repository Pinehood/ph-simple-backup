import shutil
import platform
from os import path, getenv, mkdir

from utils.helper import stripFileExtension, addTimestampToString, getParentDirPath, cleanFileLine
from utils.constants import *


def getHomePath():
  if platform.system() == OS_WINDOWS:
    return path.join(getenv(OS_ENV_APPDATA), OS_WINDOWS_DEFAULT_LOCATION)
  if platform.system() == OS_MAC:
    return path.join(getenv(OS_ENV_HOME), OS_MAC_DEFAULT_LOCATION)
  return path.join(getenv(OS_ENV_HOME), OS_LINUX_DEFAULT_LOCATION)


def extractFileName(filePath):
  return path.split(filePath)[1]


def getNewBackupPath(isFile, backupTo, sourcePath):
  backupPath = extractFileName(sourcePath)

  if isFile == True:
    backupPath = stripFileExtension(backupPath)

  backupPath = path.join(backupTo, addTimestampToString(backupPath))
  return backupPath


def updateConfig(isFile, lastFolder, lastFile, backupLocation):
  settingsPath = path.join(getHomePath(), CONFIG_FILE_NAME)
  if path.exists(settingsPath) == False:
    try: mkdir(getHomePath())
    except: print(ERROR_CREATING_FOLDER)

  isFileText = CONFIG_FALSE
  if isFile:
    isFileText = CONFIG_TRUE

  try:
    f = open(settingsPath, 'w')
    f.write(f"{CONFIG_IS_FILE}={isFileText}\n")
    f.write(f"{CONFIG_LAST_FILE}={lastFile}\n")
    f.write(f"{CONFIG_LAST_FOLDER}={lastFolder}\n")
    f.write(f"{CONFIG_BACKUP_LOCATION}={backupLocation}\n")
    f.close()
  except: print(ERROR_WRITING_SETTINGS)


def loadConfig():
  isFile = False
  lastFolder = ""
  lastFile = ""
  backupLocation = getHomePath()

  try:
    settings = open(path.join(getHomePath(), CONFIG_FILE_NAME)).readlines()
    for line in settings:
      [key, value] = line.split("=")
      if key == CONFIG_IS_FILE and cleanFileLine(value) == CONFIG_TRUE: isFile = True
      elif key == CONFIG_LAST_FOLDER: lastFolder = cleanFileLine(value)
      elif key == CONFIG_LAST_FILE: lastFile = cleanFileLine(value)
      elif key == CONFIG_BACKUP_LOCATION: backupLocation = cleanFileLine(value)
  except:
    False

  return [isFile, lastFolder, lastFile, backupLocation]


def backupFile(destinationPath, sourcePath, isFile):
  fileName = getNewBackupPath(isFile, destinationPath, sourcePath)
  try:
    shutil.make_archive(fileName, ARCHIVE_FORMAT, root_dir=getParentDirPath(sourcePath), base_dir=extractFileName(sourcePath))
    return True
  except:
    print(ERROR_BACKUP)
    return False