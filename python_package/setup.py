from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pytraffic',
      version='0.1',
      description='Traffic data collector',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Information Analysis',
      ],
      keywords='traffic bigdata collector scraping',
      author='Robert Cvitkovic',
      author_email='robert.cvitkovic@xlab.si',
      packages=find_packages(),
      install_requires=[
          'elasticsearch',
          'kafka',
          'lxml',
          'pytz',
          'requests',
      ],
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'pytraffic = pytraffic.cli:main'
          ]
      }
      )
