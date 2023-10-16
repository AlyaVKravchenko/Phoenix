from setuptools import setup, find_packages

setup(name='Phoenix',
      version='0.0.1',
      description='Your personal assistant',
      author='project-group-12',
      packages=find_packages(),
      entry_points={"console_scripts":["Ineedhelp = main:main"]},
      install_requires=["contacts", "notebook", "sorter", "re", "collections", 
                        "datetime", "pickle", "sys", "pathlib", "shutil",],
      )