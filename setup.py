from setuptools import setup,find_packages
from typing import List


def get_requirments_list()->List[str]:   #->List[str] means we are speicifying that this function will return a 
    """
    This function will return the list of requirment mentioned inside the requirments.txt file
    This funciton will return the list which will contain name of libraries mentioned in requiment.txt
    """
    
    
    with open("requirements.txt") as requirment_file: 
        return requirment_file.readlines()
                                         #list which is having string value in it. it increase the readability of
                                         #your program.  
                                         # this function will read the requirements.txt file and gets all the 
                                         # package libraries details from it and make a list of those package or
                                         #library name and return that list as result.
                                         #This list will be passed to install_requires parameter under setup()
                                         #function. 
                                         #During run time the setup() function will install all these packages and 
                                         #libraries, along with the housing package which we have specified under
                                         #packages parameter of setup() function.
   

setup(
    name="housing - predictor",   #name of your project
    version="0.0.3",              #version of your code
    author="PushpaVJ",            #Project author name
      #Even you can create the variable for all these values and pass the variable inside this function
    description="This is the housing pridiction project",
    packages=find_packages(),#['housing'], #give your project folder name
    install_requires=get_requirments_list()

)

