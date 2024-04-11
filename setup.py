from setuptools import setup, find_packages

setup(
    name="graph3d",
    version="0.0.1",
    author="Miguel Angel Ceniceros",
    description="A simple 3D plotting package made with OpenGL.",
    license="GNU GPLv3",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=["pyopengl", "numpy", "wxpython"]
)
