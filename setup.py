#!/usr/bin/env python3

from distutils.core import setup

setup(name='ipfs_handler',
      version='1.0',
      description='Python IPFS and archive toolkit',
      author='Pavel Tarasov',
      author_email='p040399@outlook.com',
      url='https://github.com/PaTara43/ipfs_handler_package',
      packages=['ipfs_handler'],
      install_requires=['IPFS-toolkit== 0.2.2',
                        'pyminizip==0.2.6',
                        'pytest~=7.0.0',
                        'PyYAML==6.0',
                        'lark==1.1.1']
      )
