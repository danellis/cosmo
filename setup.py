from setuptools import setup, find_packages
from cosmo.version import version

setup(
    name="Cosmo",
    version=version,
    packages=find_packages(),

    entry_points={
        'console_scripts': ['cosmo = cosmo.main:main']
    },

    install_requires=[
        'docutils>=0.3',
        'docopt>=0.6.2',
        'beautifulsoup4>=4.3.2',
        'requests>=2.6.2'
    ],

    tests_require=[
        'nose'
    ],

    test_suite='nose.collector',

    author="Dan Ellis",
    author_email='dan@danellis.me',
    description="Web crawler",
    license='MIT',
    keywords='web crawler spider',
    url='https://github.com/danellis/cosmo'
)
