from distutils.core import setup
setup(
    name='python3-logstash',
    packages=['logstash'],
    version='0.4.7',
    description='Python logging handler for Logstash.',
    long_description=open('README.md').read(),
    author='Israel Flores',
    author_email='jobs@israelfl.com',
    url='https://github.com/israel-fl/python3-logstash',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ]
)
