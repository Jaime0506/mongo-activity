# routes/router_car.py
from fastapi import APIRouter, HTTPException, status, Query, Response
from bson import ObjectId
from pymongo import ReturnDocument

from models.Car import Car, CarUpdate
from config.database import get_cars_collection

router = APIRouter(prefix="/cars", tags=["Cars"])

def _normalize(doc: dict) -> dict:
    """Convierte ObjectId a str para respuestas JSON."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_car(car: Car):
    """
    Crea un carro. Valida duplicados por placa.
    """
    coll = get_cars_collection()

    # Evitar placas duplicadas (opcional pero útil)
    existing = await coll.find_one({"plate": car.plate})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La placa ya existe",
        )

    data = car.model_dump(exclude_none=True)
    result = await coll.insert_one(data)
    created = await coll.find_one({"_id": result.inserted_id})
    return _normalize(created)

@router.get("/")
async def list_cars(limit: int = Query(50, ge=1, le=200)):
    """
    Lista carros (máx. 200 por petición).
    """
    coll = get_cars_collection()
    docs = await coll.find().limit(limit).to_list(length=limit)
    return [_normalize(d) for d in docs]

@router.get("/{car_id}")
async def get_car(car_id: str):
    """
    Obtiene un carro por su _id de Mongo.
    """
    coll = get_cars_collection()
    try:
        oid = ObjectId(car_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    doc = await coll.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Carro no encontrado")
    return _normalize(doc)

@router.patch("/{car_id}")
async def update_car(car_id: str, payload: CarUpdate):
    coll = get_cars_collection()
    try:
        oid = ObjectId(car_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    # Solo aplicar campos enviados
    updates = payload.model_dump(exclude_unset=True, exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="Sin cambios: no se envió ningún campo")

    # Si se cambia la placa, validamos unicidad
    if "plate" in updates:
        dup = await coll.find_one({"plate": updates["plate"], "_id": {"$ne": oid}})
        if dup:
            raise HTTPException(status_code=409, detail="La placa ya existe")

    updated = await coll.find_one_and_update(
        {"_id": oid},
        {"$set": updates},
        return_document=ReturnDocument.AFTER,
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Carro no encontrado")

    return _normalize(updated)

@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: str):
    coll = get_cars_collection()
    try:
        oid = ObjectId(car_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await coll.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Carro no encontrado")
    # 204 No Content
    return Response(status_code=status.HTTP_204_NO_CONTENT)