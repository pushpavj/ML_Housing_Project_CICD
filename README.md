# ML_Housing_Project_CICD
Housing Project with CICD pipeline

Clone the project folder from git hub
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