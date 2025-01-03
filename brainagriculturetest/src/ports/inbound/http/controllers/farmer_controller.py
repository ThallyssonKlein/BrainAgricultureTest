from fastapi import APIRouter, HTTPException
from src.application.services.example_service import ExampleService

router = APIRouter()

example_service = ExampleService()

@router.post("/farmer/")
def create_example(farmer_data: dict):
    new_example = example_service.create_example(farmer_data)
    return new_example, 201