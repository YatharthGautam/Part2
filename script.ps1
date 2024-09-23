#Deploying Azure VM 

pip install azure-mgmt-resource
pip install azure-mgmt-compute
pip install azure-mgmt-network
pip install azure-identity
az login --use-device-code
az account tenant list --output table
$env:AZURE_SUBSCRIPTION_ID ="AZURE_SUBSCRIPTION_ID"
python "c:\Users\Yatharth\OneDrive\Documents\python_scripts\Azure_VM\createVM.py"




#shell script for ReadData file 
pip install pandas
pip install openpyxl
pip install azure-storage-blob
cd /c/Users/Yatharth/OneDrive/Documents/python_scripts/Azure_VM
python ReadData.py





#storing the codes into github repo with git bash

cd  C:/Users/Yatharth/Onedrive/Documents/python_scripts/Azure_VM
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YatharthGautam/Part2.git
git push -u origin main

