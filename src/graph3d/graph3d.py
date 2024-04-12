import wx
import wx.glcanvas as glcanvas

from OpenGL.GL import *
import OpenGL.GL.shaders

from graph3d.core.setupMaterial import SetupMaterial
from graph3d.core.surface import Surface
from graph3d.core.surface import MeshGrid
from graph3d.core.renderer import Renderer
from graph3d.core.camera import Camera
from graph3d.core.scene import Scene
from graph3d.core.mesh import Mesh
from graph3d.core.axes import Axes, NAxes

import numpy as np
from math import sin, cos, tan, sqrt, pi        # for use inside eval()



class Graph3D(glcanvas.GLCanvas):

    """
    This is the Base Canvas that can be displayed on a wx.Panel.
    The arguments consist of the plotting info.
    """

    def __init__(self,
                 parent,
                 zInput:       list = [],                 # A list consisting of function strings in the form of "z = f(x, y)"
                 axRange:      tuple = (-10, 10),         # The minimum and maximum value apply for both the 'X' and 'Y' axes for the plotting area.
                 deltaXY:      int = 50,
                 colors:       list = [],                 # Specified in order of zInput
                 showAxes:     bool = True,
                 showMeshGrid: bool = True):

        self.parent = parent
        self.zInput = zInput
        self.axRange = axRange # tuple
        self.deltaXY = deltaXY
        self.colors = colors
        self.showAxes = showAxes
        self.showMeshGrid = showMeshGrid

        if self.parent == None:
            self.create_parent()

        # attribute to check if the InitGL method has been ran
        self.init = False

        # gl attributes (depth buffer, double buffer, multisampling)
        dispAttrs = glcanvas.GLAttributes()
        dispAttrs.PlatformDefaults().Depth(16).DoubleBuffer().SampleBuffers(4).Samplers(4).EndList()

        # self.size = self.GetClientSize()
        self.size = wx.Size(500, 500)

        # create canvas
        glcanvas.GLCanvas.__init__(self, self.parent, dispAttrs=dispAttrs, size=self.size)

        # create context
        self.context = glcanvas.GLContext(self)

        # assign context to canvas
        self.SetCurrent(self.context)

        # bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnPrimaryDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnPrimaryUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnSecondaryDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnSecondaryUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseDrag)

        # create frame to display graph
        if parent == None:
            self.frame.Show()
            self.app.MainLoop()


    def create_parent(self):

        self.app = wx.App()
        
        self.frame = wx.Frame(None)
        self.frame.SetTitle("3D Surface")
        self.frame.SetClientSize( self.frame.FromDIP( wx.Size(800, 600) ) )

        self.parent = self.frame
        
        
    def OnPaint(self, event):

        """
        Event handler for when the window's contents are repainted.
        """
        
        if not self.init: 
            self.InitGL()
            self.init = True
            
        self.OnDraw()
        self.SwapBuffers()

    def OnSize(self, event):

        """
        Handler for size event (when the window changes size).
        """
        
        wx.CallAfter(self.DoSetViewport)
        event.Skip()
        
    def DoSetViewport(self):

        """
        Adjust viewport using current size.
        """
        
        self.size = self.GetClientSize()
        self.window_width = self.size.width
        self.window_height = self.size.height
        self.SetCurrent(self.context)
        
        # Update camera aspect ratio and projectionMatrix
        if self.init: # if camera has already been initialized
            self.camera.aspectRatio = self.window_width / self.window_height
            self.camera.updateProjectionMatrix()

        # Set the viewport with previous values
        glViewport(0, 0, self.size.width, self.size.height)

    def OnPrimaryDown(self, event):
        try:
            self.CaptureMouse()
        except:
            pass
        self.x, self.y = self.lastx, self.lasty = event.GetPosition()

    def OnPrimaryUp(self, event):
        self.ReleaseMouse()

    def OnSecondaryDown(self, event):
        try:
            self.CaptureMouse()
        except:
            pass
        self.x, self.y = self.lastx, self.lasty = event.GetPosition()

    def OnSecondaryUp(self, event):
        self.ReleaseMouse()

    def getCameraForward(self):

        """
        Returns the camera's forward vector.
        """

        camera_model_matrix = self.camera.getWorldMatrix()
        rotation_matrix = camera_model_matrix[:3, :3]

        #r = rotation_matrix[:, 0] # right
        #u = rotation_matrix[:, 1] # up
        f = rotation_matrix[:, 2] # forward

        return f

    def lookAtOrigin(self):

        """
        Changes the camera's transform matrix to make it look at the world origin.
        """

        camera_position = self.camera.getPosition()
        target_point = np.array([0, 0, 0]) # the look target is the origin

        look_at_direction = target_point - camera_position
        look_at_direction = look_at_direction / np.linalg.norm(look_at_direction)  # normalize

        # initial up vector (positive Y)
        initial_up = np.array([0, 1, 0])

        # calculate the "right" vector (perpendicular to Y axis and
        # direction the camera should be pointing at if it were
        # pointing toward the origin
        right = np.cross(initial_up, look_at_direction)
        right = right / np.linalg.norm(right)  # normalize

        # re-orthogonalize "up" vector with new "right"
        up = np.cross(look_at_direction, right)
        up = up / np.linalg.norm(up)  # normalize

        # replace camera transform
        new_rotation_matrix = np.column_stack((right, up, -look_at_direction))
        new_camera_model_matrix = np.copy(self.camera.transform)
        new_camera_model_matrix[:3, :3] = new_rotation_matrix 
        self.camera.transform = new_camera_model_matrix
        

    def OnMouseDrag(self, event):

        """
        Handles mouse dragging events: primary click rotates and secondary click gets closer/further.
        """
        
        # Camera rotation (primary click)
        
        if event.Dragging() and event.LeftIsDown():
            
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = event.GetPosition()
            self.Refresh(False)

            # scale down mouse input
            rotation_scale = 0.01
            angle_horizontal = (self.x - self.lastx) * rotation_scale
            angle_vertical = -(self.y - self.lasty) * rotation_scale

            # get forward vector from camera
            forward = self.getCameraForward()

            # check how much is the camera pointing toward axes
            proportion_x = np.dot(forward, [1, 0, 0])
            proportion_z = np.dot(forward, [0, 0, 1])

            # calculate how much the camera should rotate around each axes
            angle_x = abs(proportion_z) * angle_vertical
            angle_z = abs(proportion_x) * angle_vertical

            # set angle sign according to quadrant (obtained by trial and error)
            if proportion_x > 0 and proportion_z > 0:
                angx = -angle_x
                angz = angle_z
            elif proportion_x > 0 and proportion_z < 0:
                angx = angle_x
                angz = angle_z
            elif proportion_x < 0 and proportion_z > 0:
                angx = -angle_x
                angz = -angle_z
            elif proportion_x < 0 and proportion_z < 0:
                angx = angle_x
                angz = -angle_z
            else:
                angx = 0
                angz = 0

            # rotate camera around all axes
            self.camera.rotateY( angle_horizontal, localCoord=False)
            self.camera.rotateZ( -angz, localCoord=False)
            self.camera.rotateX( -angx, localCoord=False)
            
            # look at origin and align with xz plane
            self.lookAtOrigin()
            
            return

        # Camera closer/further to origin. (secondary click)        
        elif event.Dragging() and event.RightIsDown():

            """
            Move the camera over the line of action from the origin to the camera itself.
            """

            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = event.GetPosition()
            self.Refresh(False)

            translation_scale = 0.2
            tval = (self.y - self.lasty) * translation_scale

            # get the direction vector from the camera position and origin
            camera_position = np.array(self.camera.getPosition())            
            origin = np.array([0, 0, 0])
            direction_vector = origin - camera_position

            # get the distance between the camera and the origin
            difference_magnitude = np.linalg.norm(direction_vector)

            # dont get too close to the origin
            if difference_magnitude < 2 and tval > 0:
                event.Skip()
                return

            # just interested in the direction
            unit_direction = direction_vector / difference_magnitude

            # scale translation vector down
            tvect = unit_direction * tval

            # translate camera over line
            self.camera.translate(tvect[0], tvect[1], tvect[2], localCoord=False)

            event.Skip()
            return
                      
    def InitGL(self):

        """
        Initialize scene and create/render surfaces.
        """
                
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(fov=35, aspectRatio=self.size.width/self.size.height, near=2.0, far=1000.0)

        # check if surface amount and color amount are the same. if
        # they are not, add random numbers for each additional
        # surface.
        
        length_zInput = len(self.zInput)
        length_colors = len(self.colors)

        # If more colors than surfaces, pass.
        # If more surfaces than colors, create additional random colors.

        while (length_zInput > length_colors):
            
            import random
            
            # create new random color 
            self.colors.append( [ random.uniform(0, 1),
                                  random.uniform(0, 1),
                                  random.uniform(0, 1) ] )

            length_colors += 1
            

        # display surfaces
        for index in range(length_zInput):

            # create function where the return value is the value of z
            # as a function of x and y, where the function is
            # specified in a string of text in zInput.
            
            def func(x, y):
                try:
                    return eval(self.zInput[index])
                except:
                    return 0

            # start and stop of both X and Y (plotting area)
            start, stop = self.axRange[0], self.axRange[1]

            # amount of iterations used in rendering triangles from surface
            # higher -> approximate surface more accurately | slower because need to calculate more vertices
            # lower  -> surface is not very accurate | faster to calculate, less vertices
            num = self.deltaXY

            # create surface geometry (points) and set material.
            geom = Surface(func, start, stop, num, color=self.colors[index])
            mat = SetupMaterial({"useVertexColors":True})
            mesh = Mesh(geom, mat)
            self.scene.add(mesh) # add surface to scene

            # show surface meshgrid. wireframe-like lines on top of actual surface.
            
            if self.showMeshGrid:

                mesh_step =  int((stop - start) / 15)
                
                geom1 = MeshGrid(func, start, stop, num, mesh_step, color=[0.1, 0.1, 0.1])
                mat1 = SetupMaterial({"useVertexColors":True,
                                      "drawMode":GL_LINES})
                mesh1 = Mesh(geom1, mat1)
                self.scene.add(mesh1)


        # 50, 150, 250 -> works for dispaired ax grid line
        length = 50
        # while the plotting range is greater than the axes length
        while (self.axRange[1] - self.axRange[0]) > length:
            length += 100

        #add positive and negative axes
        if self.showAxes:
            axes = Axes(axisLength=length)
            naxes = NAxes(axisLength=length)
            self.scene.add(axes)
            self.scene.add(naxes)
            
        # set initial camera position
        dis = 3 * (self.axRange[1] - self.axRange[0])
        self.camera.setPosition([dis, dis/2, dis])
        self.lookAtOrigin()

    def OnDraw(self):

        self.renderer.render(self.scene, self.camera)







        

        

