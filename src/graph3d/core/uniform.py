from OpenGL.GL import *

class Uniform:

    """
    Class for handling uniform data.
    """

    def __init__(self, funcRef, data):

        """
        Need to pass the function reference (funcRef) directly.
        """

        self.data = data

        # funcRef is the reference to the uniform function to be used
        # glUniform1i | glUniform1f | glUniform2f | glUniform3f | glUniform4f
        # glUniformMatrix4fv
        self.funcRef = funcRef

    def locateVariable(self, shaderProgram, variableName):

        self.variableRef = glGetUniformLocation(shaderProgram, variableName)

    def uploadData(self):

        if self.variableRef == -1:
            return

        # if the function references glUniformMatrix4fv
        if id(self.funcRef) == id(glUniformMatrix4fv):
            self.funcRef(self.variableRef, 1, GL_TRUE, self.data)
            return

        if type(self.data) == bool or type(self.data) == int:
            self.funcRef(self.variableRef, self.data)
        else:
            self.funcRef(self.variableRef, *self.data) # unpack data
        
