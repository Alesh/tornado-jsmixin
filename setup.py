import sys
from setuptools import setup, find_packages

setup(
    name = 'tornado-jsmixin',
    version = '0.2',
    zip_safe = False,
    license = "MIT License",
    packages = find_packages(),
    include_package_data = True,
    author = 'Alexey Poryadin',
    author_email = 'alexey.poryadin@gmail.com',
    url='https://github.com/Alesh/tornado-jsmixin',
    description = 'Mixins for using commonjs libs (browserify, react, ...) features within tornado.web.Application.',
    install_requires = ['Tornado', 'PyExecJS'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: JavaScript',        
    ]
)