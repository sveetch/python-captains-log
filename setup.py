from setuptools import setup, find_packages

setup(
    name='python-captains-log',
    version=__import__('captains_log').__version__,
    description=__import__('captains_log').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='sveetch@gmail.com',
    url='https://github.com/sveetch/python-captains-log',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'click==3.3',
        'colorama==0.3.2',
        'peewee==2.4.5',
        #'tabulate==0.7.3',
    ],
    entry_points={
        'console_scripts': [
            'captains-log = captains_log.cli.console_script:cli_frontend',
        ]
    },
    include_package_data=True,
    zip_safe=False
)