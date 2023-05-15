from setuptools import setup, find_packages
from codecs import open

# Get the long description from the relevant file
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='t2c',
    version='0.0.5',
    description='A Python Library that converts human readable text to Cron Expression.',
    long_description=long_description,
    url='https://github.com/iguangyu/text2cron',
    author='iguangyu',
    author_email='oofheaven7@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='text cron text langchain gpt npl',
    packages=find_packages(),
    install_requires=['pendulum', 'cn2an'],
    package_data={
        't2c': ['*.py'],
    },
)