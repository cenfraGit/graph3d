from graph3d.core.matrix import *

class Object3D:

    """
    Represents a 3D object in the scene. Holds methods for rotating and translating.
    Holds child and parent data for the object.
    """

    def __init__(self):

        self.transform = getIdentity()

        self.parent = None

        self.children = []

    def add(self, child):

        self.children.append(child)
        child.parent = self

    def remove(self, child):

        self.children.remove(child)
        child.parent = None

    # calculate transformation of this Object3D relative to the root
    # Object3D of the scene graph

    def getWorldMatrix(self):

        if self.parent == None:

            return self.transform

        else:

            return self.parent.getWorldMatrix() @ self.transform

    # return a single list containing all descendants

    def getDescendantList(self):

        descendants = []

        nodesToProcess = [self]

        while len(nodesToProcess) > 0:

            # remove first node from list
            node = nodesToProcess.pop(0)

            # add to descendant list
            descendants.append(node)

            # children of this node must also be processed
            nodesToProcess = node.children + nodesToProcess

        return descendants

    def applyMatrix(self, matrix, localCoord=True):

        if localCoord:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform

    def translate(self, x, y, z, localCoord=True):
        m = getTranslation(x, y, z)
        self.applyMatrix(m, localCoord)

    def rotateX(self, angle, localCoord=True):
        m = getRotationX(angle)
        self.applyMatrix(m, localCoord)

    def rotateY(self, angle, localCoord=True):
        m = getRotationY(angle)
        self.applyMatrix(m, localCoord)

    def rotateZ(self, angle, localCoord=True):
        m = getRotationZ(angle)
        self.applyMatrix(m, localCoord)

    def scale(self, s, localCoord=True):
        m = getScale(s)
        self.applyMatrix(m, localCoord)

    def setPosition(self, position):
        self.transform.itemset( (0, 3), position[0] )
        self.transform.itemset( (1, 3), position[1] )
        self.transform.itemset( (2, 3), position[2] )

    def getPosition(self):
        return [ self.transform.item((0, 3)),
                 self.transform.item((1, 3)),
                 self.transform.item((2, 3)) ]
        
