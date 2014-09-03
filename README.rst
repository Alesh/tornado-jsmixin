tornado-jsmixin
===============

Mixins for using commonjs libs (browserify, react, ...) features within tornado.web.Application.


Instalation
-----------

Strongly suggest using the isolated environment like this `nodeenv <https://github.com/ekalinin/nodeenv>`_.
It is important to use the latest version `PyExecJS <https://github.com/doloopwhile/PyExecJS.git>`_.
It contains an important `commit <https://github.com/doloopwhile/PyExecJS/commit/4c24fa0f5a7eb1bc965366ba2fd28c3702e153d6>`_
without which this package does not work.
::

    $ pip install git+https://github.com/doloopwhile/PyExecJS.git@master
    $ pip install git+https://github.com/Alesh/tornado-jsmixin.git@master
    $ npm install -g browserify
    $ npm install -g uglifyify
    $ npm install -g uglifycss
    $ npm install -g reactify
    $ npm install -g react


Using
-----

ReactMixin allow you to easily use react.js components written as CommonJS module in your application. 
See demo and docstrings for more detail. Documentation will comming soon.

