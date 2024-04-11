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

You can display a 3D surface in an existing wx.Panel, for example, by passing your panel reference to the `parent` argument. Or just set `parent` to `None` and the 3D graph will be shown on a new wx.Frame:

```python
Graph3D(parent=None, zInput=["cos(x)*cos(y)"])
```

# Controls
