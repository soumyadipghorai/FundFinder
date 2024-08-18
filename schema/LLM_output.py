from pydantic import BaseModel, Field  

class FundManagerDetails(BaseModel):
    pros: list[str] = Field(description="pros about the fund")
    cons: list[str] = Field(description="cons about the fund")