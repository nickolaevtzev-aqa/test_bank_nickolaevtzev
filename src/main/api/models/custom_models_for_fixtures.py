from dataclasses import dataclass

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_requesting_request import CreditRequestingRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest


@dataclass
class DepositTestContext:
	user: CreateUserResponse
	deposit: DepositRequest


@dataclass
class TransferTestContext:
	user_auth: CreateUserResponse
	from_account: CreateAccountResponse
	to_account: CreateAccountResponse
	transfer: TransferRequest


@dataclass
class CreditRequestingContext:
	user: CreateUserResponse
	credit: CreditRequestingRequest


@dataclass
class CreditRepayContext:
	user: CreateUserResponse
	repay: CreditRepayRequest
