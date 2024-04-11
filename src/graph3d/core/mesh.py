from graph3d.core.object3D import Object3D
from OpenGL.GL import *

class Mesh(Object3D):

    """
    Object that holds geometry and material data for an object.
    """

    def __init__(self, geometry, material):

        super().__init__()

        self.geometry = geometry
        self.material = material

        self.visible = True # if should be rendered or not for whatever reason

        # create vertex array object
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)

        # associate geometry variables to shader program
        for variableName, attributeObject in geometry.attributes.items():

            attributeObject.associateVariable(material.shaderProgram, variableName)

        glBindVertexArray(0) # unbind 
