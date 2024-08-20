from pydantic import BaseModel, Field  

class FundManagerDetails(BaseModel):
    """
    A data model to represent the details of a fund manager's pros and cons.
    """
    pros: list[str] = Field(description="List of pros or advantages about the fund.")
    cons: list[str] = Field(description="List of cons or disadvantages about the fund.")
