import pandas as pd
import openpyxl
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


#connecting with Azure storage account
storage_account_name = "dataengineerv1"
container_name = "raw"
blob_name = "tourism_dataset.csv"

#creating a blob service client

credendtial = DefaultAzureCredential()
blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net",credential= credendtial)

#loading the data from blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

with open("tourism_dataset.csv","wb") as download_file:
    download_file.write(blob_client.download_blob().readall())

#loading the data into the DataFrame
df = pd.read_csv("tourism_dataset.csv")

#performing data analysis on given data

     #average rating country wise
avg_country_rating = df.groupby('Country')['Rating'].mean().reset_index()
avg_country_rating.rename(columns={'Rating':'Avg rating'},inplace=True)

# Equivalent SQL Query:
# SELECT country, AVG(Rating) as AvgRating FROM tourism_dataset GROUP BY country;

     #Identify Top 3 categories with the highest average rating
top_categories = df.groupby('Category')['Rating'].mean().nlargest(3).reset_index()
top_categories.rename(columns={'Rating': 'AvgRating'}, inplace=True)

# Equivalent SQL Query:
# SELECT category, AVG(Rating) as AvgRating FROM tourism_dataset GROUP BY category ORDER BY AverageRate DESC LIMIT 3;

#Exporting the analysis results to Excel and save to VM
output_file_name = "Yatharth-Gautam.csv"
avg_country_rating.to_csv(output_file_name,index=False, header=True)

# Appending the second DataFrame with a separator
with open(output_file_name, 'a') as f:
    f.write('\n')  # Adding a new line before the next table
    top_categories.to_csv(f, index=False, header=True, lineterminator='\n')

#Uploading files to Azure Storage
upload_container_name = "yatharth-gautam"

#creating a new blob client for uploading data
upload_blob_client = blob_service_client.get_blob_client(container=upload_container_name,blob=output_file_name)

with open(output_file_name,"rb") as upload_file:
    upload_blob_client.upload_blob(upload_file, overwrite=True)

print("Analysis complete and results uploaded to Azure storage account")
