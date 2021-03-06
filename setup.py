from setuptools import setup, find_packages

setup(
    name='portube',
    version='0.0.1',
    description='Software-implemented port forwarding, transparent proxy, which can bypass firewalls in specific cases where the host restricts the inbound rules but does not restrict the outbound rules',
    author='dbsven',
    author_email='501287441@qq.com',
    license='BSD License',
    packages=find_packages(),
    py_modules=['portube'],
    platforms=["all"],
    url='https://github.com/loser007/Portube',
    keywords='portmap tunnel tube protube',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
    entry_points={
        'console_scripts': [
            'portube = portube:main',
        ]
    },
)

