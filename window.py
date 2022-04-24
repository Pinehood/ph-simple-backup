from tkinter import NORMAL, DISABLED, Menu, Tk, Button, Label, filedialog, messagebox#, PhotoImage
#from os import getcwd

from fileHandler import loadConfig, updateConfig, backupFile, extractFileName
from utils.constants import *


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


  def getNewPath(self):
    filePath = self.getFilePath()
    if filePath == "": return filePath

    return f"Backup \"{extractFileName(filePath)}\" @ {self.backupLocation}"


  def initalizeConfig(self):
    [isFile, lastFolder, lastFile, backupLocation] = loadConfig()
    self.isFile = isFile
    self.lastFolder = lastFolder
    self.lastFile = lastFile
    self.backupLocation = backupLocation


  def initalizeWindow(self):
    windowX = int((self.window.winfo_screenwidth()/2) - (APPLICATION_WIDTH/2))
    windowY = int((self.window.winfo_screenheight()/2) - (APPLICATION_HEIGHT/2))

    self.window.title(APPLICATION_TITLE)
    self.window.geometry(f"{APPLICATION_WIDTH}x{APPLICATION_HEIGHT}+{windowX}+{windowY}")
    self.window.minsize(APPLICATION_WIDTH, APPLICATION_HEIGHT)
    #self.window.iconphoto(False, PhotoImage(file=f"{getcwd()}/icon.png"))    
    self.window.resizable(0, 0)


  def initalizeComponents(self):
    backupButtonState = DISABLED
    pickFileButtonText = TEXT_CHOOSE_FOLDER
    if self.getFilePath() != "":
      backupButtonState = NORMAL
    if self.isFile:
      pickFileButtonText = TEXT_CHOOSE_FILE

    # Components initalization
    self.menuBar = Menu(self.window)
    self.settingsMenu = Menu(self.menuBar, tearoff=0)
    self.labelFile = Label(self.window, text=self.getNewPath(), wraplength=350, padx=10)
    self.buttonToggleIsFile = Button(self.window, text=TEXT_TOGGLE_IS_FILE, command=self.handleSwitchIsFileClick)
    self.buttonPickFile = Button(self.window, text=pickFileButtonText, command=self.handleChooseFileClick)
    self.buttonBackup = Button(self.window, text=TEXT_BACKUP, state=backupButtonState, command=self.handleBackupClick)

    # Dropdown menu
    self.settingsMenu.add_command(label=TEXT_CHOOSE_BACKUP_DESTINATION, command=self.handleChooseDestinationClick)
    self.settingsMenu.add_separator()
    self.settingsMenu.add_command(label=TEXT_EXIT, command=self.window.destroy)
    self.menuBar.add_cascade(label=TEXT_SETTINGS, menu=self.settingsMenu)

    # Insert components in window
    self.window.config(menu=self.menuBar)
    self.window.grid_columnconfigure(1, weight=3, minsize=210)
    self.buttonToggleIsFile.grid(row=0, column=0)
    self.buttonPickFile.grid(row=0, column=1)
    self.buttonBackup.grid(row=0, column=2)
    self.labelFile.grid(row=1, columnspan=3)


  def handleSwitchIsFileClick(self):
    if self.isFile:
      self.isFile = False
      self.labelFile[COMPONENT_TEXT] = self.getNewPath()
      self.buttonPickFile[COMPONENT_TEXT] = TEXT_CHOOSE_FOLDER
    else:
      self.isFile = True
      self.labelFile[COMPONENT_TEXT] = self.getNewPath()
      self.buttonPickFile[COMPONENT_TEXT] = TEXT_CHOOSE_FILE

    if self.getFilePath() == "":
      self.buttonBackup[COMPONENT_STATE] = DISABLED
    else:
      self.buttonBackup[COMPONENT_STATE] = NORMAL
    
    updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)


  def handleChooseFileClick(self):
    if self.isFile:
      pickedFile = filedialog.askopenfile(parent=self.window, mode="rb")
      if pickedFile != None:
        self.lastFile = pickedFile.name
        updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
        self.labelFile[COMPONENT_TEXT] = self.getNewPath()
        self.buttonBackup[COMPONENT_STATE] = NORMAL
    else:
      pickedFolder = filedialog.askdirectory(parent=self.window)
      if pickedFolder != "":
        self.lastFolder = pickedFolder
        updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
        self.labelFile[COMPONENT_TEXT] = self.getNewPath()
        self.buttonBackup[COMPONENT_STATE] = NORMAL


  def handleChooseDestinationClick(self):
    pickedLocation = filedialog.askdirectory(parent=self.window)
    if pickedLocation != "":
      self.backupLocation = pickedLocation
      updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
      self.labelFile[COMPONENT_TEXT] = self.getNewPath()


  def handleBackupClick(self):
    self.buttonBackup[COMPONENT_STATE] = DISABLED
    success = backupFile(self.backupLocation, self.getFilePath(), self.isFile)
    if success:
      self.buttonBackup[COMPONENT_STATE] = NORMAL
      messagebox.showinfo(message=TEXT_BACKUP_MSG_SUCCESS)
    else:
      if self.isFile: self.lastFile = ""
      else: self.lastFolder = ""
      self.labelFile[COMPONENT_TEXT] = self.getNewPath()
      updateConfig(self.isFile, self.lastFolder, self.lastFile, self.backupLocation)
      messagebox.showerror(message=TEXT_BACKUP_MSG_ERROR)