from graph3d.core.mesh import Mesh
from graph3d.core.geometry import Geometry
from graph3d.core.setupMaterial import SetupMaterial

from OpenGL.GL import *
import numpy as np

class Axes(Mesh):

    """
    Positive axes mesh object.
    """

    def __init__(self,
                 axisLength=1,    # Length of X, Y, Z axes
                 lineWidth=2,     # Axes line width
                 axisColors=[ [1, 0, 0], [0, 0, 1], [0, 1, 0] ]): # Red, Blue, Green because of switching Y with Z.

        geom = Geometry()
        
        positionData = [ [0, 0, 0], [axisLength, 0, 0],
                         [0, 0, 0], [0, axisLength, 0],
                         [0, 0, 0], [0, 0, axisLength] ]

        colorData = [axisColors[0], axisColors[0],
                     axisColors[1], axisColors[1],
                     axisColors[2], axisColors[2]]

        # --------------------------------------------------- LINE INDICATORS (display positive integers)

        ax_line_size = 0.3  
        x_range = np.arange(1, axisLength+1, 1) # [1, 2, 3, 4, ..., 50]

        # x indicators
        for i in range(len(x_range)):
            if i == len(x_range)-1:
                break
            p1 = [ x_range[i], 0, -ax_line_size ]
            p2 = [ x_range[i], 0,  ax_line_size ]
            positionData.append(p1)
            positionData.append(p2)
            colorData.append(axisColors[0])
            colorData.append(axisColors[0])

        # y indicators
        for i in range(len(x_range)):
            if i == len(x_range)-1:
                break
            p1 = [-ax_line_size, 0, x_range[i] ]
            p2 = [ ax_line_size, 0, x_range[i] ]
            positionData.append(p1)
            positionData.append(p2)
            colorData.append(axisColors[2])
            colorData.append(axisColors[2])

        # z indicators
        for i in range(len(x_range)):
            if i == len(x_range)-1:
                break
            p1 = [ -ax_line_size, x_range[i], 0]
            p2 = [  ax_line_size, x_range[i], 0 ]
            positionData.append(p1)
            positionData.append(p2)
            colorData.append(axisColors[1])
            colorData.append(axisColors[1])

        # add attributes for position and color
        geom.addAttribute(3, GL_FLOAT, "vertexPosition", positionData)
        geom.addAttribute(3, GL_FLOAT, "vertexColor", colorData)
        
        geom.countVertices()

        # setup material
        mat = SetupMaterial({"useVertexColors":1, "lineWidth":lineWidth, "drawMode":GL_LINES})

        # initialize mesh object
        super().__init__(geom, mat)



class NAxes(Mesh):

    """
    Negative axes mesh object.
    """

    def __init__(self, axisLength=1, lineWidth=2, axisColors=[ [0.6, 0, 0], [0, 0, 0.6], [0, 0.6, 0] ]):

        geom = Geometry()

        positionData = []
        colorData = []

        # for line segmentation
        num = axisLength+1
        nrange = np.linspace(0, -axisLength, num)

        # --------------------------------------------------- LINE INDICATORS

        ax_line_size = 0.3
        x_range = np.arange(1, axisLength+1, 1) # [1, 2, 3, 4, ..., 50]

        # x indicators
        for i in range(len(x_range)):
            if i == len(x_range)-1:
                break
            p1 = [ -x_range[i], 0, -ax_line_size ]
            p2 = [ -x_range[i], 0,  ax_line_size ]
            positionData.append(p1)
            positionData.append(p2)
            colorData.append(axisColors[0])
            colorData.append(axisColors[0])

        # y indicators
        for i in range(len(x_range)):
            if i == len(x_range)-1:
                break
            p1 = [-ax_line_size, 0, -x_range[i] ]
            p2 = [ ax_line_size, 0, -x_range[i] ]
            positionData.append(p1)
            positionData.append(p2)
            colorData.append(axisColors[2])
            colorData.append(axisColors[2])

        # z indicators
        for i in range(len(x_range)):
            if i == len(x_range)-1:
                break
            p1 = [ -ax_line_size, -x_range[i], 0]
            p2 = [  ax_line_size, -x_range[i], 0 ]
            positionData.append(p1)
            positionData.append(p2)
            colorData.append(axisColors[1])
            colorData.append(axisColors[1])

        # ----------------------------------------------------- axes

        # x values
        for i in range(num):
            if i % 2 == 0: # segment line
                continue
            if i == len(nrange) - 2: # to keep pair of lines for each axes
                break
            point = [ nrange[i], 0, 0 ]
            positionData.append(point)
            colorData.append(axisColors[0])

        # y values
        for i in range(num):
            if i % 2 == 0: # segment line
                continue
            if i == len(nrange) - 2: # to keep pair of lines for each axes
                break
            point = [ 0, nrange[i], 0 ]
            positionData.append(point)
            colorData.append(axisColors[1])

        # z values
        for i in range(num):
            if i % 2 == 0: # segment line
                continue
            if i == len(nrange) - 2: # to keep pair of lines for each axes
                break
            point = [ 0, 0, nrange[i] ]
            positionData.append(point)
            colorData.append(axisColors[2])

        # add attributes for position and color
        geom.addAttribute(3, GL_FLOAT, "vertexPosition", positionData)
        geom.addAttribute(3, GL_FLOAT, "vertexColor", colorData)
        
        geom.countVertices()

        # setup material
        mat = SetupMaterial({"useVertexColors":1, "lineWidth":lineWidth, "drawMode":GL_LINES})

        # initialize mesh object.
        super().__init__(geom, mat)
