import shutil
import platform
from datetime import datetime
from os import path, getenv
from constants import *

def getHomePath():
  if platform.system() == OS_WINDOWS:
    return path.join(getenv(OS_ENV_APPDATA), OS_WINDOWS_DEFAULT_LOCATION)
  if platform.system() == OS_MAC:
    return path.join(getenv(OS_ENV_HOME), OS_MAC_DEFAULT_LOCATION)
  return path.join(getenv(OS_ENV_HOME), OS_LINUX_DEFAULT_LOCATION)

def getFullFileName(filePath):
  fileNameParts = filePath.split("/")
  return fileNameParts[len(fileNameParts) - 1]

def getFileLocation(filePath):
  filePathParts = filePath.split("/")
  filePathParts.pop()
  return "/".join(filePathParts)

def stripFileExtension(file):
  fileNameParts = file.split(".")
  fileName = ""

  for i in range(len(fileNameParts)):
    if len(fileNameParts)-1 != i:
      fileName += fileNameParts[i]
  return fileName

def getNewArchiveName(fileName):
  return f"{datetime.now().strftime(DATE_FORMAT)}-{fileName}"

def updateConfig(isFile, lastFolder, lastFile, backupLocation):
  isFileText = CONFIG_FALSE
  if isFile:
    isFileText = CONFIG_TRUE
  try:
    f = open(path.join(getHomePath(), CONFIG_FILE_NAME), 'w')
    f.write(f"{CONFIG_IS_FILE}={isFileText}\n")
    f.write(f"{CONFIG_LAST_FILE}={lastFile}\n")
    f.write(f"{CONFIG_LAST_FOLDER}={lastFolder}\n")
    f.write(f"{CONFIG_BACKUP_LOCATION}={backupLocation}\n")
  except:
    False

def cleanFileLine(line):
  return line.replace("\n", "").strip()

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
  fileName = ""
  if isFile:
    fileName = f"{destinationPath}/{getNewArchiveName(stripFileExtension(getFullFileName(sourcePath)))}"
  else:
    fileName = f"{destinationPath}/{getNewArchiveName(getFullFileName(sourcePath))}"

  try:
    shutil.make_archive(fileName, "zip", root_dir=getFileLocation(sourcePath), base_dir=getFullFileName(sourcePath))
    return True
  except:
    return False