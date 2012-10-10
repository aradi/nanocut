Installation
============

Download
--------

The latest version of Nanocut can be downloaded from
`http://bitbucket.org/aradi/nanocut/ <http://bitbucket.org/aradi/nanocut/>`_. 


Install
-------

Nanocut is written in Python3 and uses the great NumPy package. In order
to install and run it, you need therefore:

* Python version 3.2 or later
* NumPy version 1.6.2 or later

You can install the program using the standard Python package installation
procedure. If you want to install Nanocut to the standard python package
location (you may need root rights for that), you can issue::

  python3 setup.py install

in the root directory of Nanocut. Otherwise, you can specify a location
prefix. For example to install it somewhere in your HOME-directory::

  python3 setup.py install --prefix ~/opt/nanocut

In this case make sure, your ``PYTHONPATH`` environment variable contains the
appropriate ``site-packages`` folder with the Nanocut packages. When using the
BASH shell, you could issue::

  export PYTHONPATH=$PYTHONPATH:~/opt/nanocut/lib/python3.2/site-packages

provided you're using Python version 3.2. The Nanocut executable (``nanocut``)
will be placed into the diretory ``/home/username/opt/nanocut/bin``.

You can check your installation by invoking Nanocut. Issuing::

  ~/opt/nanocut/bin/nanocut -h

should give you a short summary about the command line options of the
program. If you get error messages about missing modules instead, make sure you
use the right version of Python and NumPy and you set up your environment as
explained above.

