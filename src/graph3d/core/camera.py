from graph3d.core.object3D import Object3D
from graph3d.core.matrix import *
from numpy.linalg import inv

class Camera(Object3D):

    """
    Holds camera data. 
    """

    def __init__(self, fov=60, aspectRatio=1, near=0.1, far=1000):

        super().__init__()

        self.fov = fov
        self.aspectRatio = aspectRatio
        self.near = near
        self.far = far

        self.projectionMatrix = None
        self.updateProjectionMatrix()

        self.viewMatrix = getIdentity()

    def updateProjectionMatrix(self):

        self.projectionMatrix = getPerspective(self.fov, self.aspectRatio, self.near, self.far)
        

    def updateViewMatrix(self):

        self.viewMatrix = inv(self.getWorldMatrix())
