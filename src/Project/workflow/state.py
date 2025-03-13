from pydantic import BaseModel
from typing import List, Dict, Any

class State(BaseModel):
    messages: List[Dict[str, Any]] = []