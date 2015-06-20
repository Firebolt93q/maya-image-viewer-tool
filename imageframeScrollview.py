import maya.cmds as cmds
import os
import os.path
from functools import partial
import maya.OpenMaya as OpenMaya
import maya.mel as mel

##
# main class for setting up UI
##        
class MasterWindow(object):
    def __init__(self):
        self.title = "Izzy Image Viewer"
        self.imageElementsList = []
        
        # delete current instance of window
        if cmds.window('masterWindow', exists=True):
            cmds.deleteUI('masterWindow')
        if cmds.dockControl('IzzyImageViewer', exists=True):
            cmds.deleteUI('IzzyImageViewer')
        
        # formatting
        masterWindow = cmds.window('masterWindow', title='masterWindow', resizeToFitChildren=False)
        form = cmds.formLayout(parent=masterWindow, numberOfDivisions=100) 
        allowedAreas = ['all']
        masterDockControl = cmds.dockControl('IzzyImageViewer', area='left', content=masterWindow, allowedArea=allowedAreas, sizeable=True)
        
        mainScrollLayout = cmds.scrollLayout(parent = form)  
        cmds.formLayout(form, edit=True,
        attachForm=(
                    [mainScrollLayout, 'top', 10],
                    [mainScrollLayout, 'left', 0],
                    [mainScrollLayout, 'right', 0],
                    [mainScrollLayout, 'bottom', 2]
                    )
        )
        
        self.scrollingFormLayout = cmds.formLayout(parent = mainScrollLayout, numberOfDivisions=100)

        btn = cmds.button(parent = self.scrollingFormLayout, label='Add New Image', command=self.onAddNewImage, width=200, height=30)
        
        self.imagesScrollLayout = cmds.scrollLayout(parent = self.scrollingFormLayout, width = 400, height = 100)
        
        self.currentImage = cmds.image(parent = self.scrollingFormLayout)
        
        cmds.formLayout(self.scrollingFormLayout, edit=True,
                        attachForm=(
                                    [btn, 'top', 10],
                                    [self.imagesScrollLayout, 'top', 100],
                                    [self.currentImage, 'top', 200]
                                    
                                    )
                        )

        

   ##
   # callback for Add New Image button is pressed
   ##
    def onAddNewImage(self, *args):
        imageFilter = "All Files(*.*)"
        filePaths = cmds.fileDialog2(dialogStyle = 2, fileMode=1, fileFilter=imageFilter)
        if filePaths:
            newImageElement = self.createImageElement(filePaths[0])
            if newImageElement:
                self.updateScrollLayout(newImageElement)
   ##
   # create a new image element given a file path and return the element
   ##
    def createImageElement(self, filePath):
        newImageElement = imageElement(filePath)
        imageRef = OpenMaya.MImage()
        try:
            imageRef.readFromFile(filePath)
            scriptUtil = OpenMaya.MScriptUtil()
            widthPtr = scriptUtil.asUintPtr()
            heightPtr = scriptUtil.asUintPtr()
            imageRef.getSize(widthPtr, heightPtr)
            width = scriptUtil.getUint(widthPtr)
            height = scriptUtil.getUint(heightPtr)  
            newImageElement.width = width
            newImageElement.height = height 
            print "Izzy Image Viewer: Got reference image %s" % newImageElement.path
        except:
            print "Izzy Image Viewer: ERROR GETTING IMAGE REFERENCE"
            pass
        return newImageElement
        
   ##
   # update what is inside scroll layout with image buttons
   ##
    def updateScrollLayout(self, newImageElement):
        self.imageElementsList.append(newImageElement)
        cmds.scrollLayout(self.imagesScrollLayout, edit=True, childResizable = True, height = 100, width=400)
        cmds.button(parent = self.imagesScrollLayout, label=newImageElement.name, command=partial(self.onShowImage, newImageElement))
        print "Izzy Image Viewer: successfully updated scroll layout!"
        
   ##
   # callback for when an image button in scroll layout is pressed
   ##
    def onShowImage(self, *args):
        imageElement = args[0]
        cmds.image(self.currentImage, width=imageElement.width, height=imageElement.height, e=True, image=imageElement.path, parent=self.scrollingFormLayout)
        print "Izzy Image Viewer: Now viewing %s" % imageElement.name
            
    
    
##
# class for image element object
##    
class imageElement(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.width = None
        self.height = None
        if self.path:
            self.createSuccess()
    
    def createSuccess(self):
        print "Izzy Image Viewer: %s was added to the image viewer." % self.name    

########################

MasterWindow()
