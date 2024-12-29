echo [$(date)]: "START"
echo [$(date)]: "creating env with python 3.11 version" 
conda create  --prefix ./gemstone_env1 python=3.11.4 -y
echo [$(date)]: "activating the environment" 
source activate ./gemstone_env1
echo [$(date)]: "installing the dev requirements" 
pip install -r requirements_dev.txt
echo [$(date)]: "END" 