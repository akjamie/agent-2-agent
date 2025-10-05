from pydantic import BaseModel

class AgentInput(BaseModel):
    input_data: str

class AgentOutput(BaseModel):
    result: str

