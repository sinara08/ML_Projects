from setuptools import find_packages,setup

REQUIREMENT_FILE_NAME  = 'requirements.txt'
HYPHEN_E_DOT = '-e .'
def get_requirements()->list[str]:
    """
    This function will return list of requirements
    """
    with open(REQUIREMENT_FILE_NAME) as req_file:
        req_list = req_file.readlines()
    req_list =  [req.replace('\n','') for req in req_list]
    if HYPHEN_E_DOT in req_list:
        req_list.remove(HYPHEN_E_DOT)

    return req_list

setup(
    name="sensor",
    version="0.0.1",
    author="ineuron",
    author_email="avnish@ineuron.ai",
    packages = find_packages(),
    install_requires=get_requirements(),#["pymongo==4.2.0"],
)