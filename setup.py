from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tools',
    version='0.1.0',
    packages=find_packages(exclude='tests'),
    url='',
    license=license,
    author='bryandunlap',
    author_email='bryandunlap@gmail.com',
    description='Assembler and emulator for SAP-2 (upward compatible with Intel 8085 instruction set)',
    long_description=readme
)
