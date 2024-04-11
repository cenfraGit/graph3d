from OpenGL.GL import *
import numpy as np

class Attribute:

    """
    Class for handling attributes and associating them with shader variables.
    """

    def __init__(self, dataSize, dataType, data):

        self.dataSize = dataSize    # 1, 2, 3, 4

        self.dataType = dataType    # GL_INT | GL_FLOAT

        self.data = data            # Array of data to be stored in buffer

        self.bufferRef = glGenBuffers(1)

        self.uploadData()

    def uploadData(self):

        """
        Load data to attribute buffer.
        """

        data = np.array(self.data, dtype = np.float32)                    # Convert to NumPy array

        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)                     # Bind buffer as array buffer

        glBufferData(GL_ARRAY_BUFFER, data.flatten(), GL_STATIC_DRAW)     # Store data in buffer

    def associateVariable(self, shaderProgram, variableName):

        """
        Associate attribute to the variable in the shader program.
        """

        variableRef = glGetAttribLocation(shaderProgram, variableName)    # Get reference

        if variableRef == -1:
            return

        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef) # Bind attribute buffer

        glVertexAttribPointer(variableRef, self.dataSize, self.dataType, False, 0, None)   # Specify how data will be read

        glEnableVertexAttribArray(variableRef)          # Indicate that data will be streamed to this variable

        
