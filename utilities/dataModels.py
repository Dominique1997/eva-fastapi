from pydantic import BaseModel
from utilities.settings import Settings


class ReadCommand(BaseModel):
    OSType: str = ""
    command: str = ""
