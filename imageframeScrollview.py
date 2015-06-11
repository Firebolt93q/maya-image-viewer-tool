import maya.cmds as cmds
import os
import os.path
from functools import partial

# Class for main window that will be docked
#
class masterWindow(object):
    def __init__(self):
        self.imageElements = []
        self.currentImagePath = ""
        self.masterWindow = ""
        self.masterDockControl = ""
        
    # main function to refresh window
    #
    def showMasterWindow(self):
        masterWindow = cmds.window()
        form = cmds.formLayout(parent=masterWindow, numberOfDivisions=2)
        allowedAreas = ['all']
        
        masterDockControl = cmds.dockControl(area='left', content=masterWindow, allowedArea=allowedAreas )
    
        cmds.rowColumnLayout()
        cmds.scrollLayout(childResizable = False, height = 100, width=400)
        
        for iElement in imageElements:
            cmds.button(label=iElement.name, command=partial(onShowImage, iElement.path))
        
        cmds.setParent("..")
        
        cmds.button(label="Add New Image", command=onAddNewImage)
        
        if currentImagePath:
            print "switch images"
            cmds.image('currentImage', image=currentImagePath, width=800, height=800) 
                
        cmds.showWindow(masterWindow)
    
    
    ## Definitions for helper functions
    ##
    def onAddNewImage(*args):
        imageFilter = "All Files (*.*)"
        filePaths = cmds.fileDialog2(dialogStyle = 2, fileMode=1, fileFilter=imageFilter)
        #imageElement = createImageElement() #change this to handle more than one image
        
        newImageElement = createImageElement(filePaths[0])
        imageElements.append(newImageElement)
        cmds.deleteUI(masterDockControl)
        cmds.deleteUI(masterWindow)    
    
        showMasterWindow()
        print newImageElement.name 
        print newImageElement.path
    
    
    def createImageElement(filePath):
       newImageElement = imageElement(filePath)
       return newImageElement
       
    def onShowImage(path, *args):
        currentImagePath = path
        cmds.deleteUI(masterDockControl)
        cmds.deleteUI(masterWindow)
        showMasterWindow()
       

## Class for image element that will go in the list of images
##
class imageElement(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
    
    def createSuccess(self):
        print "%s was created." % self.name
        

mw = masterWindow()
mw.showMasterWindow()

 