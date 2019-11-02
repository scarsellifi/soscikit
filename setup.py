from setuptools import setup

setup(name='SoSciKit',
      version='0.2.3',
      description='Social Science Kit - Open Source Software for Social Science',
      url='',
      author='Marco Scarselli',
      author_email='scarselli@gmail.com',
      license='MIT',
      packages=['soscikit'],
      include_package_data=True,
      install_requires=[
          "pandas==0.25.1",
          "flask",
          "seaborn",
          "numpy",
          "scipy",
          "uuid==1.30",
          "matplotlib",
          "pandas_profiling",
          "altair",
          "xlrd==1.1.0",
          "jupyter"
      ],
      zip_safe=False)
