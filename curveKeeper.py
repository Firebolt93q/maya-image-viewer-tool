import maya.cmds as mc

if mc.window("curveKeeperWindow", ex=True):
    mc.deleteUI("curveKeeperWindow", window=True)
        
mc.window("curveKeeperWindow", t="Curve Keeper", wh=(100,500), s=True)

topFormLayout = mc.formLayout()
topTabsLayout = mc.tabLayout()

mc.formLayout(topFormLayout, edit=True, attachForm=[(topTabsLayout, "top", 10),
                                                    (topTabsLayout, "bottom", 10),
                                                    (topTabsLayout, "left", 10),
                                                    (topTabsLayout, "right", 10)
                                                    ])
#first tab                                               
addCurve_layout = mc.columnLayout()
mkCurve_shelf = mc.shelfLayout(w=500, h=200)

mkCurve_shelf = mc.symbolButton(image = "saveCurveIcon.png", w=150, h=150, c="")

mc.setParent("..")
mc.setParent("..")

#second tab
savedCurves_layout = mc.columnLayout()
savedCurves_shelf = mc.shelfLayout(w=500, h=200)


mc.showWindow("curveKeeperWindow")





#testCurve = mc.curve(d=1, p=[(0, 0, -2), (-2, 0, 0), (0, 0, 2), (2, 0, 0),(0, 0, -2)])

#preserve the points of the curve from selection
selectionList = mc.ls(type="nurbsCurve")

#test the first one selected
saveCurve(selectionList[0])





#number of CVs = degree + spans.
def saveCurve(curveToSave):
    spans = mc.getAttr(curveToSave + ".spans")
    degrees = mc.getAttr(curveToSave + ".degree")
    
    numOfCVs = spans + degrees
    pointsList = []
    
    for i in range(0, numOfCVs, 1):
        cv = mc.getAttr(curveToSave + ".cv[%d]" % i)
        #pointsList.append(cv)
        pointsList.append((cv[0]))
        print cv[0]
    
    mc.curve(d=1, p=pointsList)
    print "Saved Curve!"
    
    
    
    
    
    
    
