from graph3d.core.object3D import Object3D

class Scene(Object3D):

    """
    Represents the entire scene. Will not be rendered, just serves
    as a parent object for the objects in the scene.

    """

    def __init__(self):

        super().__init__()
