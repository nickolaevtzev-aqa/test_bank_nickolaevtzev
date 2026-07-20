from typing import Annotated

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class TransferRequest(BaseModel):
	fromAccountId: int
	toAccountId: int
	amount: float
