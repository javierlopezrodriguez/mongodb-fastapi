# mongodb-fastapi
RESTful API using FastAPI to connect to a MongoDB database.

# Contents of this repository:
This repository contains a starter project that demonstrates the integration of FastAPI, a modern web framework for building APIs in Python, with MongoDB, a NoSQL document-oriented database. The project provides a simple API for managing flower data, showcasing basic CRUD operations (Create, Read, Update, Delete) with MongoDB as the data storage (provided as a cloud service by an Atlas MongoDB cluster).

It is based on this tutorial (https://www.mongodb.com/languages/python/pymongo-tutorial), with some modifications.

## models.py
Definition of the data models using Pydantic to handle the data validation and serialization for the MongoDB + FastAPI application.
The models are defined to support the following non-tabular data:
```yaml
    {
        "_id": "64c1d7c991e84e28c735a5c6",
        "sepal": {
            "length": 5.1,
            "width": 3.5
            },
        "petal": {
            "length": 1.4,
            "width": 0.2
            },
        "species": "Iris-setosa"
    }
```
It contains models for Sepal, Petal and Flower (for creation, where every field except for the ID is required), and for SepalUpdate, PetalUpdate and FlowerUpdate (where every field is optional).
The serialization and validation of MongoDB's BSON ObjectId is handled by annotating it, to make it compatible with Pydantic, behaving like a string.
(See https://stackoverflow.com/questions/76686267/what-is-the-new-way-to-declare-mongo-objectid-with-pydantic-v2-0)

## routes.py
The REST API Endpoints are implemented in routes.py. 
- List all entries in the database. (GET /flower)
- Upload a new entry into the database. (POST /flower)
- Find an entry by its id. (GET /flower/{id})
- Update some fields from an entry given its id. It allows for partial and complete updates, except for the id field which cannot be modified. (PUT /flower/{id})
- Delete an entry given its id. (DELETE /flower/{id})

## main.py
The main file, where the event handlers establish and close the MongoDB connection on startup and shutdown. The Endpoints from routes.py are registered here as well.

## upload.py
Script to upload the Iris dataset from iris.csv into the MongoDB database, using the REST API.

## .env
Environment variables, accessed through the dotenv library.
The ATLAS_URI needs to be modified to include your own connection string (see #Do it yourself).

## example.ipynb
A notebook to exemplify the use of the REST API to Create, Read, Update and Delete from the MongoDB database.
It contains examples of the basic CRUD opperations allowed by the Endpoints defined in routes.py.

## iris.csv
A very famous dataset, which contains 3 classes of 50 instances each, where each class refers to a type of iris plant.
Available from UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/53/iris).

# Do it yourself:
## Create the virtual environment:
```
python -m venv pymongo-fastapi
source pymongo-fastapi/bin/activate
python -m pip install 'fastapi[all]' 'pymongo[srv]' python-dotenv requests ipykernel
python -m ipykernel install --user --name=pymongo-fastapi
```

## MongoDB Atlas cluster:
You can create a free account here: 
https://www.mongodb.com/docs/atlas/getting-started/
Atlas provides a MongoDB database on the cloud, for free, with access to many tools and resources.

Once you have created the database, in the project's .env file, you need to substitute <username> for your username, <password> for your password, and complete the rest of the connection string. 

### Getting the connection string
In Atlas, go to Data Services. On the left, click Databases. Find your Database Deployment, click Connect, and Connect with MongoDB Driver. 
Your connection string will appear in the pop up window.

## Run the Rest API:
```
source pymongo-fastapi/bin/activate
python -m uvicorn main:app --reload
```

## Fill the database with the Iris dataset:
```
source pymongo-fastapi/bin/activate
python upload.py
```

## Run the examples in the Jupyter Notebook
Connect to the pymongo-fastapi kernel, make sure you have uvicorn running so that your REST API is online, and run the notebook.
It contains examples for all the CRUD operations.
