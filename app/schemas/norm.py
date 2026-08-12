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
