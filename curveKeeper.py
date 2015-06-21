import maya.cmds as mc

#testCurve = mc.curve(d=1, p=[(0, 0, -2), (-2, 0, 0), (0, 0, 2), (2, 0, 0),(0, 0, -2)])
#preserve the points of the curve

#number of CVs = degree + spans.
spans = mc.getAttr("curve1.spans")
degrees = mc.getAttr("curve1.degree")

numOfCVs = spans + degrees
pointsList = []

for i in range(0, numOfCVs, 1):
    cv = mc.getAttr("curve1.cv[%d]" % i)
    #pointsList.append(cv)
    pointsList.append((cv[0]))


print pointsList

testCurve = mc.curve(d=1, p=pointsList)