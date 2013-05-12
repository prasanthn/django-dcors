import dcors

from setuptools import setup, find_packages


setup(
    name='django-dcors',
    version=dcors.__version__,
    description="Django middleware for adding CORS HTTP headers.",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=['django', 'CORS'],
    author='Prasanth Nair',
    author_email='prasanth.n@outlook.com',
    url='http://github.com/prasanthn/django-dcors',
    license='MIT',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
)
