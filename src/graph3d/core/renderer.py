from OpenGL.GL import *
from graph3d.core.mesh import Mesh
from graph3d.core.axes import Axes, NAxes
from graph3d.core.surface import MeshGrid

class Renderer:

    """
    Handles the rendering process. 
    """

    def __init__( self, clearColor=[0, 0, 0] ):


        glClearDepth(1.0)
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1)
        
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LEQUAL)
        glDepthRange(0.0, 1.0)

        glEnable(GL_MULTISAMPLE)

    def render(self, scene, camera):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # update camera view matrix
        camera.updateViewMatrix()

        descendantList = scene.getDescendantList()
        meshFilter = lambda x: isinstance(x, Mesh)
        meshList = list( filter( meshFilter, descendantList) )

        for mesh in meshList:
            
            if not mesh.visible:
                continue

            # use shader program to render
            glUseProgram(mesh.material.shaderProgram)

            # bind vao
            glBindVertexArray(mesh.vaoRef)

            # update uniform values stored outside of material
            mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix

            # update uniforms stored in material
            for variableName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()

            # update render settings
            mesh.material.updateRenderSettings()

            # if the mesh is a MeshGrid object, disable depth testing (to better display meshgrid from surface)
            if isinstance(mesh, MeshGrid):
                glDisable(GL_DEPTH_TEST)
            else:
                glEnable(GL_DEPTH_TEST)
                
            # if the mesh instance is the positive or negative axes, disable depth testing to that they appear in front of everything.
            # axes objects will be added to scene last, so they will be on top of meshgrids too.
            if isinstance(mesh, Axes) or isinstance(mesh, NAxes):
                glDisable(GL_DEPTH_TEST)
            else:
                glEnable(GL_DEPTH_TEST)

            # draw array using specified drawMode.
            glDrawArrays(mesh.material.settings["drawMode"], 0, mesh.geometry.vertexCount)
            

            
