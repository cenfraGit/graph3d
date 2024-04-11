# graph3d
A simple 3D plotting package made with OpenGL. It uses wxPython to display OpenGL graphics. Its main purpose is interactability as opposed to other plotting packages focused more on generating graphs that are used in academic papers or other types of documents.

![test](imgs/cap4.JPG?raw=true "Cap4")

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

Surfaces are represented with Z as a function of X and Y (for example: "2 * x * y", where z is not written in the string). There are obvious downsides to this, but this approach was selected for the sake of an intuitive and easy-to-use tool.

You can display a 3D surface in an existing wx.Panel by passing your panel reference to the `parent` argument. Or just set `parent` to `None` and the 3D graph will be shown on a new wx.Frame:

```python
Graph3D(parent=None, zInput=["cos(x)*cos(y)"])
```

![test](imgs/cap1.JPG?raw=true "Cap1")

To add more surfaces, add them to the `zInput` list as strings:

```python
Graph3D(parent=None, zInput=[ "cos(x) * cos(y)", "0.3 * x * y" ])
```

![test](imgs/cap2.JPG?raw=true "Cap2")

Whenever a color is not specified (or there are more surfaces than colors specified), a random color will be applied to the surface. The colors are written as RGB, where each value ranges from 0 to 1. To specify a color for the surfaces, add them in the same order to the `colors` argument:

```python
Graph3D(parent=None, zInput=[ "cos(x) * cos(y)", "0.3 * x * y" ], colors=[ [0, 0, 0.8] , [0.3, 0.2, 0.5] ])
```

![test](imgs/cap3.JPG?raw=true "Cap3")

There are a couple of additional parameters you can set. `deltaXY` specifies the resolution for the figure. Basically, it increases or decreases the amount of triangles that the surfaces in the scene will have. `showMeshGrid` is used to hide/show the wireframe-like lines shown on top of the surface itself. I recommend leaving it on because otherwise the figure shape may not be as easily recognized since lighting is not yet implemented. `showAxes` just hides or shows the 3D axes (which by the way, the axes with the segmented lines represent the negative axes and the ones with the solid lines represent the positive axes).

```python
Graph3D(parent=None, 
        zInput=["cos(x) * cos(y)", "0.3 * x * y"], 
        colors=[ [0, 0, 0.8] , [0.3, 0.2, 0.5] ],
        deltaXY=30,
        showMeshGrid=False,
        showAxes=False)
```

The `deltaXY` parameter is particularly useful to render more accurately-shaped surfaces, but use it carefully since a high value can cause a lot of overhead and is not always necessary.

# Controls
Use your primary click to rotate the camera around the origin.
Hold your secondary click and move your mouse vertically to move the camera closer to / farther away from the origin.

# Issues

One of the most important limitations of this package and its approach to rendering surfaces using a z = "f(x, y)" input is that the value of `z` cannot be squared and therefore cannot fully represent some surfaces such as spheres, ellipsoids, etc. The workaround for this problem is plotting the same surface twice but explicitely adding a negative sign to one of the functions so that it appears  negative. This problem is inherent to all functions that are symmetric to XY plane.

For example, in order to plot a sphere we would do the following:

```python
Graph3D(parent=None, 
        zInput=["sqrt( 100 - x**2 - y**2 )", "-sqrt( 100 - x**2 - y**2 )"], 
        colors=[ [0.8, 0, 0] , [0, 0, 0.8]], # these two colors would have to be the same
        axRange=(-10, 10),
        deltaXY=300) # a high value is better for sphere-like objects
```

![test](imgs/cap5.JPG?raw=true "Cap5")



There are some other features such as number lines along the axes, legends, graph titles, lighting, spherical coordinates, etc. that are currently missing. These may or may not be added in the future.


