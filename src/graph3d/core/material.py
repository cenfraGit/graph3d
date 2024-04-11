from graph3d.core.uniform import Uniform
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

class Material:

    """
    Class for handling the appearance of mesh objects.
    """

    def __init__(self, vertexShaderCode, fragmentShaderCode):

        # compile shaders
        vertexShader = compileShader(vertexShaderCode, GL_VERTEX_SHADER)
        fragmentShader = compileShader(fragmentShaderCode, GL_FRAGMENT_SHADER)

        # compile program
        self.shaderProgram = compileProgram(vertexShader, fragmentShader)

        # set up material uniforms
        self.uniforms = {}

        # initialize matrices
        self.uniforms["modelMatrix"] = Uniform(glUniformMatrix4fv, None)
        self.uniforms["viewMatrix"] = Uniform(glUniformMatrix4fv, None)
        self.uniforms["projectionMatrix"] = Uniform(glUniformMatrix4fv, None)

    def addUniform(self, funcRef, variableName, data):

        self.uniforms[variableName] = Uniform(funcRef, data)

    def locateUniforms(self):

        for variableName, uniformObject in self.uniforms.items():

            uniformObject.locateVariable(self.shaderProgram, variableName)

    def updateRenderSettings(self):

        pass

    def setProperties(self, properties):

        """
        For setting additional material properties when initializing.
        """

        for name, data in properties.items():

            if name in self.uniforms.keys():
                self.uniforms[name].data = data

            elif name in self.settings.keys():
                self.settings[name] = data

