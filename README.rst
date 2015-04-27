This repository contains example code and utility scripts for using the External
API that is exposed by Smart Shooter. More information about Smart Shooter can
be found at:

* `<http://kuvacode.com>`_
* `<http://kuvacode.com/smart-shooter/documentation/external-api>`_

The External API itself does not impose any restrictions on what programming
language can be used. The API operates by communicating over a socket managed by
`ZeroMQ <http://zeromq.org>`_, using `JSON <http://json.org>`_ as the message
format.

The example scripts demonstrate how the API can be used from Python, but these
can be used as a reference for other languages.

Installing Python on Windows
----------------------------

To run the examples on Windows, Python must be installed, along with the
`pyzmq <https://github.com/zeromq/pyzmq/blob/master/README.md>`_ python package
(for using ZeroMQ). The latest version of Python can be downloaded from
`<http://python.org/downloads>`_. It's recommended to install version 3.4 or
later.

Once Python is installed, open a command prompt. Check that the newly installed
``python.exe`` is in your PATH. Python will also have added ``pip.exe``, which
is used to install new python packages. This is located in the *Scripts*
subdirectory of the Python installation, so also add this directory to you PATH.
For example::

    set PATH=C:\Python34;C:\Python34\Scripts;%PATH%

Then to install pyzmq::

    pip install pyzmq

Now to run one of the examples::

    python utils/smartshooter-ls.py
