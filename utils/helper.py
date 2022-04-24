from datetime import datetime

from utils.constants import DATE_FORMAT


def stripFileExtension(file):
  fileNameParts = file.split(".")
  fileName = ""

  for i in range(len(fileNameParts)):
    if len(fileNameParts)-1 != i:
      fileName += fileNameParts[i]

  return fileName


def getParentDirPath(path):
  pathParts = path.split("/")
  pathParts.pop()
  return "/".join(pathParts)


def addTimestampToString(name):
  return f"{datetime.now().strftime(DATE_FORMAT)}-{name}"


def cleanFileLine(line):
  return line.replace("\n", "").strip()
