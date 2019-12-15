from setuptools import setup, find_packages


setup(
    name='brainstorm',
    version='0.1.0',
    author='Shachaf Ben Jakov',
    description='Main project in Advanced-System-Design course',
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest'],
)
