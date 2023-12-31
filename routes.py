# Implement the REST API endpoints
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Flower, FlowerUpdate

# Router
router = APIRouter()

# POST /flower
# API Endpoint for inserting new flower entries (documents) into the flowers database.
@router.post("/", response_description="Create a new flower", status_code=status.HTTP_201_CREATED, response_model=Flower)
def create_flower(request: Request, flower: Flower = Body(...)):
    db = request.app.database["flowers"] # access the MongoDB database
    flower = jsonable_encoder(flower) # encode flower into json
    new_flower = db.insert_one(flower) # insert into db
    # autogenerated id of the new flower is in new_flower.inserted_id
    # output the inserted flower with its id
    created_flower = db.find_one(
        {"_id": new_flower.inserted_id}
    )
    return created_flower

# GET /flower
# API Endpoint for getting a list with all documents in the flowers collection
@router.get("/", response_description="List all flowers", response_model=List[Flower])
def list_flowers(request: Request):
    # find 10 documents (flower) from the flowers collection
    # Access the MongoDB database
    db = request.app.database["flowers"]
    # Find 100 documents (flowers) from the flowers collection
    flowers = list(db.find(limit=10))
    return flowers

# GET /flower/{id}
# API Endpoint for getting a single flower (document) from the flowers database (collection) given its id.
@router.get("/{id}", response_description="Get a single flower by id", response_model=Flower)
def find_flower(id: str, request: Request):
    # Access the MongoDB database
    db = request.app.database["flowers"]
    # return the flower if it is found
    if (flower := db.find_one({"_id": id})) is not None:
        # := combines assignment and condition check
        return flower
    # raise exception if no document was found
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flower with ID {id} not found")

# Helper function to update Flower
# This is necessary so that a partial update of a field inside a nested dictionary
# does not remove the non-updated fields of that nested dictionary
# Input:
# {"species": "Iris-updated","sepal": {"width": 9}}
# Output:
# {'$set': {'species': 'Iris-updated', 'sepal.width': 9.0}} 
def get_flower_update_query(flower_update: FlowerUpdate):

    # Handle partial update for the top-level fields (species)
    top_level_fields = {k: v for k, v in flower_update.dict().items() if v is not None and k not in ["sepal", "petal"]}

    # Handle partial update for the nested fields (sepal)
    if flower_update.sepal:
        sepal_fields = {f"sepal.{k}": v for k, v in flower_update.sepal.dict().items() if v is not None}
    else:
        sepal_fields = {}

    # Handle partial update for the nested fields (petal)
    if flower_update.petal:
        petal_fields = {f"petal.{k}": v for k, v in flower_update.petal.dict().items() if v is not None}
    else:
        petal_fields = {}

    update_query = {"$set": {**top_level_fields, **sepal_fields, **petal_fields}}
    # $set operator will only update the fields that are included.
    return update_query

# PUT /flower/{id}
# API Endpoint for updating a single flower from the database.
@router.put("/{id}", response_description="Update a flower", response_model=Flower)
def update_flower(id: str, request: Request, flower: FlowerUpdate = Body(...)):
    # Access the MongoDB database
    db = request.app.database["flowers"]
    # Generate the update query based on the provided FlowerUpdate model
    update_query = get_flower_update_query(flower)
    # if there is any field to update:
    if len(update_query) >= 1:
        # updates the specified fields 
        update_result = db.update_one({"_id": id}, update_query)

        if update_result.modified_count == 0:
            # if the database was not modified, it means there was no flower with that ID
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flower with ID {id} not found")
    # if there is a flower with the provided ID, return it (after the possible update)
    if (
        existing_flower := db.find_one({"_id": id})
    ) is not None:
        return existing_flower
    # raise exception if no document was found
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flower with ID {id} not found")

# DELETE /flower/{id}
# API Endpoint for deleting a single flower (document) from the database.
@router.delete("/{id}", response_description="Delete a flower")
def delete_flower(id: str, request: Request, response: Response):
    # Access the MongoDB database
    db = request.app.database["flowers"]
    # delete the flower with the given id
    delete_result = db.delete_one({"_id": id})
    # if one document was deleted
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        # 204 No Content: status code to indicate that the deletion was successful without including a response body
        return response
    else: # raise exception if no document was deleted
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flower with ID {id} not found")
    
# /flower endpoints need to be registered on the main.py file