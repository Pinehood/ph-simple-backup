from tkinter import NORMAL, DISABLED, Tk, Button, Label, filedialog, messagebox
from fileutils import loadConfig, updateConfig, backupFile
from constants import *

class Window:
  def __init__(self):
    self.window = Tk()

    self.initalizeConfig()
    self.initalizeWindow()
    self.initalizeComponents()

    self.window.mainloop()

  def getFilePath(self):
    if self.isFile == True:
      return self.lastFile
    return self.lastFolder
  
  def toggleIsFile(self):
    if self.isFile:
      self.isFile = False
      self.buttonToggleIsFile["text"] = TEXT_SWITCH_TO_FILE
    else:
      self.isFile = True
      self.buttonToggleIsFile["text"] = TEXT_SWITCH_TO_FOLDER

  def initalizeConfig(self):
    [isFile, lastFolder, lastFile, backupLocation] = loadConfig()
    self.isFile = isFile
    self.lastFolder = lastFolder
    self.lastFile = lastFile
    self.backupLocation = backupLocation

  def initalizeWindow(self):
    self.window.title(APPLICATION_TITLE)
    self.window.geometry(APPLICATION_SIZE)
    self.window.resizable(0, 0)

  def initalizeComponents(self):
    backupButtonState = DISABLED
    toggleButtonText = TEXT_SWITCH_TO_FILE
    pickFileButtonText = TEXT_CHOOSE_FOLDER
    if self.getFilePath() != "":
      backupButtonState = NORMAL
    if self.isFile:
      toggleButtonText = TEXT_SWITCH_TO_FOLDER
      pickFileButtonText = TEXT_CHOOSE_FILE

    self.labelFile = Label(self.window, text=self.getFilePath())
    self.labelDestination = Label(self.window, text=self.backupLocation)
    self.buttonToggleIsFile = Button(self.window, text=toggleButtonText, command=self.handleSwitchIsFileClick)
    self.buttonPickFile = Button(self.window, text=pickFileButtonText, command=self.handleChooseFileClick)
    self.buttonPickDestination = Button(self.window, text=TEXT_CHOOSE_BACKUP_DESTINATION, command=self.handleChooseDestinationClick)
    self.buttonBackup = Button(self.window, text=TEXT_BACKUP, state=backupButtonState, command=self.handleBackupClick)

    self.buttonToggleIsFile.pack()
    self.labelFile.pack()
    self.buttonPickFile.pack()
    self.labelDestination.pack()
    self.buttonPickDestination.pack()
    self.buttonBackup.pack()

  def handleSwitchIsFileClick(self):
    self.toggleIsFile()

    if self.isFile:
      self.labelFile["text"] = self.lastFile
      self.buttonPickFile["text"] = TEXT_CHOOSE_FILE
    else:
      self.labelFile["text"] = self.lastFolder
      self.buttonPickFile["text"] = TEXT_CHOOSE_FOLDER

    if self.getFilePath() == "":
      self.buttonBackup["state"] = DISABLED
    else:
      self.buttonBackup["state"] = NORMAL
    
    updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)

  def handleChooseFileClick(self):
    if self.isFile:
      pickedFile = filedialog.askopenfile(parent=self.window, mode="rb")
      if pickedFile != None:
        self.lastFile = pickedFile.name
        updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
        self.labelFile["text"] = pickedFile.name
        self.buttonBackup["state"] = NORMAL
    else:
      pickedFolder = filedialog.askdirectory(parent=self.window)
      if pickedFolder != "":
        self.lastFolder = pickedFolder
        updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
        self.labelFile["text"] = pickedFolder
        self.buttonBackup["state"] = NORMAL

  def handleChooseDestinationClick(self):
    pickedLocation = filedialog.askdirectory(parent=self.window)
    if pickedLocation != "":
      self.backupLocation = pickedLocation
      updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
      self.labelDestination["text"] = self.backupLocation

  def handleBackupClick(self):
    self.buttonBackup["state"] = DISABLED
    success = backupFile(self.backupLocation, self.getFilePath(), self.isFile)
    if success:
      self.buttonBackup["state"] = NORMAL
      messagebox.showinfo(message=TEXT_BACKUP_MSG_SUCCESS)
    else:
      if self.isFile:
        self.lastFile = ""
      else:
        self.lastFolder = ""
      self.labelFile["text"] = self.getFilePath()
      updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
      messagebox.showerror(message=TEXT_BACKUP_MSG_ERROR)