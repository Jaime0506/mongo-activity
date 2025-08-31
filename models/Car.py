from pydantic import BaseModel, Field
from typing import Optional

class Car(BaseModel):
    year: int = Field(..., gt=2000, description="Año del modelo, debe ser mayor a 2000")
    model_name: str = Field(..., min_length=5, description="Nombre del modelo (mínimo 5 caracteres)")
    description: str = Field(..., min_length=10, description="Descripción del carro (mínimo 10 caracteres)")
    plate: str = Field(..., min_length=6, max_length=6, pattern="^[A-Z]{3}[0-9]{3}$", description="Placa colombiana en formato ABC123")

class CarUpdate(BaseModel):
    year: int | None = Field(None, gt=2000, description="Año del modelo, debe ser mayor a 2000")
    model_name: str | None = Field(None, min_length=5, description="Nombre del modelo (mínimo 5 caracteres)")
    description: str | None = Field(None, min_length=10, description="Descripción del carro (mínimo 10 caracteres)")
    plate: str | None = Field(None, min_length=6, max_length=6, pattern="^[A-Z]{3}[0-9]{3}$", description="Placa colombiana en formato ABC123")