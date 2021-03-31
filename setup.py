import setuptools

short_description = """\
Two classes used for creating a command-line driven menu interface"""

try:
  with open("README.md", "r") as readme:
    long_description = readme.read()
except:
  long_description = short_description

classifiers = ["Programming Language :: Python :: 3",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Development Status :: 5 - Production/Stable",
               "Environment :: Console"]

setuptools.setup(name = "py_menu",
                 version = "1.2.1",
                 author = "John Gresl",
                 author_email = "j.gresl12@gmail.com",
                 description = "Command-line driven menu interface in python",
                 long_description = long_description,
                 long_description_content_type = "text/markdown",
                 url = "https://github.com/SyntaxVoid/py_menu",
                 packages = ["py_menu"],
                 package_dir = {"py_menu": "py_menu"},
                 package_data = {"py_menu": ["examples/*"]},
                 classifiers = classifiers,
                 python_requires = ">=3.0")
