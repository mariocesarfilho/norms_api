from pydantic import BaseModel

from app.schemas.norm import NormData


class DashboardActTypeItem(BaseModel):
    act_type: str
    total: int


class DashboardAgencyItem(BaseModel):
    agency_unit: str
    total: int


class DashboardData(BaseModel):
    total_norms: int
    total_act_types: int
    total_agencies: int

    by_act_type: list[DashboardActTypeItem]
    by_agency: list[DashboardAgencyItem]

    norms: list[NormData]


class DashboardResponse(BaseModel):
    success: bool
    message: str
    data: DashboardData