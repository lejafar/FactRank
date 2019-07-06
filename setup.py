from setuptools import setup

setup(name='factrank',
      version='1.0.0',
      packages=['factrank'],
      install_requires=['pyyaml',
                        'numpy',
                        'torch==1.1.0',
                        'dickens',
                        'torchtext',
          ]
)
