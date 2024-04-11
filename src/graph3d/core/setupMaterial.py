from graph3d.core.material import Material
from graph3d.core.uniform import Uniform

import os
from OpenGL.GL import *


class SetupMaterial(Material):

    """
    Base setup material for meshes. Can be modified according to type of mesh (axes, meshgrid, surfaces).
    """

    def __init__(self, properties={}):

        vertexShaderCode = """
        #version 330
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        out vec3 color;

        void main()
        {
          gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
          color = vertexColor;
        }
        """

        fragmentShaderCode = """
        #version 330
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        in vec3 color;
        out vec4 fragColor;

        void main()
        {
                vec4 tempColor = vec4(baseColor, 1.0);

                if (useVertexColors)
                  tempColor = vec4(color, 1.0);

                fragColor = tempColor;
        }
        """

        # initialize material (will compile shaders and program)
        super().__init__(vertexShaderCode, fragmentShaderCode)

        # configure base color (unnecesary, vertex colors are always used)
        self.addUniform( glUniform3f, "baseColor", [1, 0, 0] )
        self.addUniform( glUniform1i, "useVertexColors", False ) # initialize uniform for material setting
        self.locateUniforms()

        # material settings dictionary
        self.settings = {} 

        # default material setting values
        self.settings["drawMode"] = GL_TRIANGLES
        self.settings["lineWidth"] = 1
        self.settings["pointSize"] = 2

        self.setProperties(properties)

    def updateRenderSettings(self):

        """
        Update values from settings dictionary.
        """

        # culling is disabled so that both sides from the surface can be seen
        glDisable(GL_CULL_FACE)
        glLineWidth(self.settings["lineWidth"])
        glPointSize(self.settings["pointSize"])
        
