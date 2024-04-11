from graph3d.core.attribute import Attribute

class Geometry:

    """
    Used for handling position and color data attributes.
    """

    def __init__(self):

        self.attributes = {}

        self.vertexCount = None

    def addAttribute(self, dataSize, dataType, variableName, data):

        """
        dataSize -> 3 (for position, for example, [x, y, z])
        dataType -> GL_FLOAT | GL_INT
        variableName -> shader variable name
        data     -> array of data
        """

        self.attributes[variableName] = Attribute(dataSize, dataType, data)

    def countVertices(self):

        attrib = list(self.attributes.values())[0]
        self.vertexCount = len(attrib.data)
