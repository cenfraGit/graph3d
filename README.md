# graph3d
A simple 3D plotting package made with OpenGL. It uses wxPython to display the OpenGL context.

# Installation
Run the following line in the terminal to create the .tar.gz file:

```
python setup.py sdist
```

Then install using pip:

```
pip install ./dist/graph3d-0.0.1.tar.gz
```

# Usage

Import the package with:

```python
from graph3d.graph3d import Graph3D
```

Surfaces are represented with Z as a function of X and Y (for example: 2 * x * y, where z is not written in the string). There are obvious downsides to this, but this approach was selected for the sake of an intuitive and easy-to-use tool.

You can display a 3D surface in an existing wx.Panel by passing your panel reference to the `parent` argument. Or just set `parent` to `None` and the 3D graph will be shown on a new wx.Frame:

```python
Graph3D(parent=None, zInput=["cos(x)*cos(y)"])
```

![test](imgs/cap1.JPG?raw=true "Cap1")

To add more surfaces, add them to the `zInput` list as strings:

```python
Graph3D(parent=None, zInput=[ "cos(x) * cos(y)", "0.3 * x * y" ])
```

Whenever a color is not specified (or there are more surfaces than colors specified), a random color will be applied to the surface. The colors are written as RGB, where each value ranges from 0 to 1. To specify a color for the surfaces, add them in the same order to the `colors` argument:

```python
Graph3D(parent=None, zInput=[ "cos(x) * cos(y)", "0.3 * x * y" ], colors=[ [0, 0, 0.8] , [0.3, 0.2, 0.5] ])
```

There are a couple of additional parameters you can set. `deltaXY` specifies the resolution for the figure. Basically, it increases or decreases the amount of triangles that the surfaces in the scene will have. `showMeshGrid` is used to hide/show the wireframe-like lines shown on top of the surface itself. I recommend leaving it on because otherwise the figure shape may not be as easily recognized since lighting is not yet implemented. `showAxes` just hides or shows the 3D axes (which by the way, the axes with the segmented lines represent the negative axes and the ones with the solid lines represent the positive axes).

```python
Graph3D(parent=None, 
        zInput=["cos(x) * cos(y)", "0.3 * x * y"], 
        colors=[ [0, 0, 0.8] , [0.3, 0.2, 0.5] ],
        deltaXY=30,
        showMeshGrid=False,
        showAxes=False)
```

You can use these parameters to your advantage if you are going to plot surfaces that would be drawn with spherical coordinates (which this package does not yet support). This would 

# Controls
