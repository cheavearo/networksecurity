'''
The setup.py file is an essential part of packageing and distribution Python projects. 
It is used by setup tools (or distutils in older Python version)
to define the configuration of your project, such as its metadata, dependencies and more.
'''


from setuptools import find_packages, setup
from typing import List

requirement_lst:List[str]=[]

def get_requirements() ->List[str]:
    '''
    THis function will return list of requirement
    '''
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from the file
            lines=file.readlines()
            # Process each line
            for line in lines:
                requirement=line.strip()
                ### Ignore the empty lines and -e.
                if requirement and requirement!='-e.':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file are not found")
    return requirement_lst

setup(
    name="NetworkSecurity",
    version="0.0.2",
    autho="Vearo",
    packages=find_packages(),
    install_requires=get_requirements()
)
