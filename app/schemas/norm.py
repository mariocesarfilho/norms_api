from pydantic import BaseModel

class NormBase(BaseModel):
    act_type: str
    act_number: int
    agency_unit: str
    publication: str
    summary: str

class NormCreate(NormBase):
    pass

class NormData(NormBase):
    id: int
    class Config:
        from_attributes = True

class NormResponse(BaseModel):
    success: bool
    message: str
    data: NormData

class NormListResponse(BaseModel):
    success: bool
    message: str
    data: list[NormData]

class NormUpdate(BaseModel):
    act_type: str | None = None
    act_number: int | None = None
    agency_unit: str | None = None
    publication: str | None = None
    summary: str | None = None
