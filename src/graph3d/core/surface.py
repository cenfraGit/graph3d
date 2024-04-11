from graph3d.core.geometry import Geometry
from OpenGL.GL import *
import numpy as np

class MeshGrid(Geometry): # will not create triangles, just lines

    """
    Wireframe-like object that renders on top of surface. Useful because lighting is not yet implemented.
    """

    def __init__(self,
                 function:str,      # string -> value of z, function of x and y. e.g. "2*x**2"
                 start:int = -10,
                 stop:int = 10,
                 num:int = 50,
                 step:int = 1,
                 color:list = [1, 0, 0]):

        super().__init__()

        positionData = []
        colorData = []

        x_list = np.linspace(start, stop, num)
        y_list = np.linspace(start, stop, num)

        x_integers = np.arange(start, stop, step)
        y_integers = np.arange(start, stop, step)
        
        #for i in range(num-1):
        for i in x_integers:

            for j in range(num-1):

                # heights
                h1 = function(i, y_list[j])
                h2 = function(i, y_list[j+1])

                if h1 == 0 and h2 == 0:
                    continue

                positionData.append([i, h1, y_list[j]])
                positionData.append([i, h2, y_list[j+1]])

                colorData.append(color)
                colorData.append(color)

        for j in y_integers:
            for i in range(num-1):

                # heights
                h1 = function(x_list[i], j)
                h2 = function(x_list[i+1], j)                

                if h1 == 0 and h2 == 0:
                    continue

                positionData.append([x_list[i], h1, j])
                positionData.append([x_list[i+1], h2, j])

                colorData.append(color)
                colorData.append(color)                
                
        self.addAttribute(3, GL_FLOAT, "vertexPosition", positionData)
        self.addAttribute(3, GL_FLOAT, "vertexColor", colorData)

        self.countVertices()
    

class Surface(Geometry):

    def __init__(self,
                 function:str, # string -> value of z as a function of x, y.
                 start:int = -10,
                 stop:int = 10,
                 num:int = 50, # deltaXY -> determines the amount of iterations to render pair of triangles.
                 color:list = [1, 0, 0]):

        super().__init__()

        positionData = []
        colorData = []

        # used for creating the 'meshgrid' plotting area
        x_list = np.linspace(start, stop, num)
        y_list = np.linspace(start, stop, num)
        
        # for every grid square
        for i in range(num-1):

            for j in range(num-1):

                # calculate z values of each corner of the grid square
                z1 = function(x_list[i], y_list[j])
                z2 = function(x_list[i], y_list[j+1])
                z3 = function(x_list[i+1], y_list[j+1])
                z4 = function(x_list[i+1], y_list[j])

                # create points of each of the grid squares including height of z value.
                p1 = [x_list[i], y_list[j], z1]
                p2 = [x_list[i], y_list[j+1], z2]
                p3 = [x_list[i+1], y_list[j+1], z3]
                p4 = [x_list[i+1], y_list[j], z4]

                # changed y and z coordinates order (OpenGL's up vector is Y and we want it to be Z because math standard)
                p1 = [x_list[i], z1, y_list[j]]
                p2 = [x_list[i], z2, y_list[j+1]]
                p3 = [x_list[i+1], z3, y_list[j+1]]
                p4 = [x_list[i+1], z4, y_list[j]]

                z_val = p4 # p4 is the height value of current iteration grid.

                # if z value is 0, the
                # part of the surface is not supposed to be plot.
                # therefore, do not create vertices and skip iteration.
                if z_val[1] == 0 and ( (p1[1] == 0) and (p2[1] == 0) and (p3[1] == 0) ):
                    continue

                # if all triangle vertices are 0, do not draw triangle.

                # first triangle
                if (p1[1] == 0) and (p2[1] == 0) and (z_val[1] == 0):
                    pass
                else: # draw triangle
                    # positions
                    positionData.append( p1 )
                    positionData.append( p2 )
                    positionData.append( z_val )
                    # colors
                    for c in range(3):
                        colorData.append(color)

                # second triangle
                if (p2[1] == 0) and (p3[1] == 0) and (z_val[1] == 0):
                    pass
                else: # draw triangle
                    # positions
                    positionData.append( p2 )
                    positionData.append( p3 )
                    positionData.append( z_val )
                    # colors
                    for c in range(3):
                        colorData.append(color)                    
                
                            
        self.addAttribute(3, GL_FLOAT, "vertexPosition", positionData)
        self.addAttribute(3, GL_FLOAT, "vertexColor", colorData)

        self.countVertices()

        

        
