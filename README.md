# ML_Housing_Project_CICD
Housing Project with CICD pipeline

## Clone the project folder from git hub
git clone https://github.com/pushpavj/ML_Housing_Project_CICD.git

Create conda environment
conda create -p venv python==3.7 -y

Activate the conda environment
conda activate venv/

update .gitignore file to specify venv/

Create requirments.txt and specify 
Flask
gunicorn 

Install requirements.txt
pip install -r requirenments.txt

Create app.py file 

create docker file

create dockerignore file and specify .gitinore, venv, .git

create .github folder
create workflows folder inside .github
create main.yaml file

push all the changes to github

check the git remote name and its associated url
git remote -v

check the git status
git status

add the changes to git
git add .

commit the git changes
git commit -m "initial commit"

push the changes to git
git push origin main

Starting with ML-Housing Project with established CICD pipeline
Create a new folder with name housing.

Outside the housing folder create the setup.py file.

Under housing folder create __init__.py. The housing folder will be a root folder and it will be created as a package and we can use it any where we want by importing it.

start coding setup.py file. 

This setup.py is used to install our project folder as package and also with this we can install the libraries mentioned under requirements.txt file. Inside the setup.py code will be written to read the requirements.txt file and get the list of libraries to be installed. We need not to do pip install -r requirements.txt. 
Along with this we also specify the details of project name, author, description of the project under setup() function. 


python setup.py install #to execute setup.py and install the required libraries. With this we need not to
install requirements.txt seperately. 

Once the setup.py is installed it automatically creates certain files and folders inside your project folder as shown below, such as build,dist, housing_prdictor.egg-info

When ever you make changes to requirments.txt file or any thing inside the setup.py file, in order to 
reexecute and install setup.py again then before execution you need to change the version number inside
setup.py file code.


you can open the ipynb file through vscode and execute your commands as in jupyternotes for that you need to isntall the ipykernel

pip install ipykernel

You need to choose the same conda environment as your housing project, in my case it has automatically considered housing project environment venv only. If it is not selected then if you click on the environment icon in this case venv we can see list of available environments and from that list we need to select our project environment.


to read yaml file
pip install PyYAML