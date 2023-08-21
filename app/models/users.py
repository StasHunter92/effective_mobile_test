from pydantic import BaseModel


# ----------------------------------------------------------------------------------------------------------------------
# Create models
class User(BaseModel):
    """
    Pydantic user model
    """
    id: int
    last_name: str
    first_name: str
    patronymic: str
    organization: str
    organization_phone_number: str
    phone_number: str
