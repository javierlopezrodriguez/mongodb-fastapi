from dotenv import dotenv_values
import requests
import csv

config = dotenv_values(".env")
# converts the .env file contents into a dictionary

# Example entry
""" {
    "sepal": {"length": 5.1, "width": 3.5},
    "petal": {"length": 1.4, "width": 0.2},
    "species": "Iris-setosa"
} """

# Open the csv file 
with open("iris.csv", "r") as csvf:
    for entry in csv.DictReader(csvf):
        new_flower = {}
        # rename class to species
        new_flower["species"] = entry["class"]
        # get sepal length and width into the appropriate format
        new_flower["sepal"] = {
            "length": entry["sepal_length"],
            "width": entry["sepal_width"]
        }
        # get petal length and width into the appropriate format
        new_flower["petal"] = {
            "length": entry["petal_length"],
            "width": entry["petal_width"]
        }

        # insert the entry into the database using the REST API
        response = requests.post(f'{config["FASTAPI_URL"]}/flower/', json=new_flower)

print("Done!")