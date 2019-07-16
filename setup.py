from setuptools import setup, find_packages
import os

def readme():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')) as f:
        return f.read()

setup(
    name='batchproc',
    version='0.1.1',
    packages=find_packages(exclude=['tests*']),
    install_requires=['doit'],
    url='https://github.com/metavee/batchproc',
    license='MIT',
    author='Robin Neufeld',
    author_email='raeneufe@uwaterloo.ca',
    description='Simple batch processing framework.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)
