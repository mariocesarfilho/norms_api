from pydantic import BaseModel

class NormBase(BaseModel):
    act_type: str
    act_number: int
    agency_unit: str
    publication: str
    summary: str

class NormCreate(NormBase):
    pass

class NormResponse(NormBase):
    id: int
    class Config:
        from_attributes = True
