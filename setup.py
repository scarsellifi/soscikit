from setuptools import setup

setup(name='SoSciKit',
      version='0.4.0',
      description='Social Science Kit - Open Source Software for Social Science',
      url='https://github.com/scarsellifi/soscikit',
      author='Marco Scarselli',
      author_email='scarselli@gmail.com',
      license='MIT',
      keywords = ["Social Science", "Software", "Data", "Analysis"],
      packages=['soscikit'],
      include_package_data=True,
      install_requires=[
          "pandas>=0.25.1",
          "flask",
          "seaborn",
          "numpy",
          "scipy",
          "uuid==1.30",
          "matplotlib",
          "pandas_profiling",
          "altair",
          "xlrd==1.1.0",
          "jupyter",
          "openpyxl"
      ],
      long_description="""
          # SoSciKit
            ## Social Science Kit - Open Source Software for Social Science
            
            SoSciKit is a web application for simplified data analysis based on Python scientific libraries and Flask.
            The web application allows to use the python libraries through a graphical interface even to those who do not know programming language. At the moment the application allows to perform monovariate, bivariate, cross tabulation and k-mean classification operations. In addition, it allows to recode categorical variables and create typologies.
            
            [![Downloads](https://pepy.tech/badge/soscikit)](https://pepy.tech/project/soscikit)
            [![Downloads](https://pepy.tech/badge/soscikit/week)](https://pepy.tech/project/soscikit/week)
            
            ## Installation and dependencies
            You need a python interpeter installed on PC / Server. 
            You need Python 3 (tested 3.6 - 3.7) to run this package. Other dependencies can be found in the requirements files
            
            ### Using pip
            
            You can install using the pip package manager by running
            
                pip3.x install soscikit
            
            ## Usage
            
            You can start SoScikit by running
            
                python3.x -m soscikit
            
            it's start server and open your browser on localhost http://127.0.0.1:5555/
            
            
            ## How to contribute
            
            The package is actively maintained and developed as open-source software. If SoSciKit was helpful or interesting to you, you might want to get involved. There are several ways of contributing and helping. If you would like to be a industry partner or sponsor, please [drop us a line](mailto:scarselli@gmail.com).
            
            ## Demo
            
            You can try a [DEMO](http://soscikit.eu.pythonanywhere.com/)
          
          """,
      long_description_content_type='text/markdown',
      zip_safe=False)
