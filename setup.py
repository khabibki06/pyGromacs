from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='pyGromacs',
    url='https://github.com/khabibki06/pyGromacs',
    author='khabib khumaini',
    author_email='khabibki06@gmail.com',
    # Needed to actually package something
    packages=['pyGromacs'],
    # Needed for dependencies
    install_requires=['numpy', 'pandas', 'matplotlib'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='UP',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
