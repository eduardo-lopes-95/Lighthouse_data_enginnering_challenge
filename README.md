# Indicium Code Challenge - Eduardo Sabino
Indicium code challenge for Software Developer focusing on data projects

# The Challenge

We are going to provide 2 data sources, a Postgres database and a CSV file.

The CSV file represents details of orders from a ecommerce system.

The database provided is a sample database provided by microsoft for education purposes called northwind, the only difference is that the order_detail table does not exists in this database you are beeing provided with.This order_details table is represented by the CSV file we provide.

Schema of the original Northwind Database: 

![image](https://user-images.githubusercontent.com/49417424/105997621-9666b980-608a-11eb-86fd-db6b44ece02a.png)

Your mission is to build a pipeline that extracts the data everyday from both sources and write the data first to local disk, and second to a database of your choice. For this challenge, the CSV file and the database will be static, but in any real world project, both data sources would be changing constantly.


Its important that all writing steps are isolated from each other, you shoud be able to run any step without executing the others.

For the first step, where you write data to local disk, you should write one file for each table and one file for the input CSV file. This pipeline will run everyday, so there should be a separation in the file paths you will create for each source(CSV or Postgres), table and execution day combination, e.g.:

```
/data/postgres/{table}/2021-01-01/file.format
/data/postgres/{table}/2021-01-02/file.format
/data/csv/2021-01-02/file.format
```

you are free to chose the naming and the format of the file you are going to save.

At step 2, you should load the data from the local filesystem to the final database that you chosed. 

The final goal is to be able to run a query that shows the orders and its details. The Orders are placed in a table called **orders** at the postgres Northwind database. The details are placed at the csv file provided, and each line has an **order_id** field pointing the **orders** table.

How you are going to build this query will heavily depend on which database you choose and how you will load the data this database.

The pipeline will look something like this:

![image](https://user-images.githubusercontent.com/49417424/105993225-e2aefb00-6084-11eb-96af-3ec3716b151a.png)

## Things that Matters

- Clean and organized code.
- Good decisions at which step (which database, which file format..) and good arguments to back those decisions up.

## Setup of the source database

The source database can be set up using docker compose.
You can install following the instructions at 
https://docs.docker.com/compose/install/

With docker compose installed simply run

```
docker-compose up
```

You can find the credentials at the docker-compose.yml file

## Final Instruction

You can use any language you like, but keep in mind that we will have to run your pipeline, so choosing some languague or tooling that requires a complex environment might not be a good idea.
You are free to use opensource libs and frameworks, but also keep in mind that **you have to write code**. Point and click tools are not allowed.


# Lets get started


## Chosen database 

Step 2 will be performed by extracting the data from the local disk and uploading it to Bigquery (datawarehouse hosted by Google Cloud). 

To connect and authenticate uploads in Bigquery, a service account with write permissions was created and from this service account an access key was generated that inherits these permissions.

With the client libraries and the access key, you can instantiate a bigquery.Client() class and thus perform read and write operations.

link to documentation:
> https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=pt-br#client-libraries-install-python

## Install packages 
```
pip install -r ./requirements.txt
```

## Instructions on how to run the  pipeline
- Execution: 
    
    ```
    py main.py <Parameter 1> <Parameter 2>
    ```
    - **Parameter 1** (mandatory):
        - **-e**: to run only step 1 
        - **-l**: to run only step 2 
        - **-b**: to run both steps
    - **Parameter 2** (optional):
        - date in format **YYYY-MM-DD**
        - If date was not defined, its will consider current date