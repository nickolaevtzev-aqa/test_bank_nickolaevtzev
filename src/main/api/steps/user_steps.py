from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.custom_models_for_fixtures import *
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
	def create_account(self, create_user_request: CreateUserRequest):
		response = ValidatedCrudRequester(
				RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
				Endpoint.CREATE_ACCOUNT,
				ResponseSpecs.request_created()
		).post()
		return response

	def deposit(self, deposit_request: DepositTestContext):
		response = ValidatedCrudRequester(
			RequestSpecs.auth_headers(username=deposit_request.user.username, password=deposit_request.user.password),
			Endpoint.DEPOSIT,
			ResponseSpecs.request_ok()
		).post(deposit_request.deposit)
		return response

	def deposit_invalid(self, deposit_request: DepositTestContext):
		response = CrudRequester(
			RequestSpecs.auth_headers(username=deposit_request.user.username, password=deposit_request.user.password),
			Endpoint.DEPOSIT,
			ResponseSpecs.request_bad()
		).post(deposit_request.deposit)
		return response

	def transfer(self, context: TransferTestContext):
		auth = context.user_auth
		response = ValidatedCrudRequester(
				RequestSpecs.auth_headers(username=auth.username, password=auth.password),
				Endpoint.TRANSFER,
				ResponseSpecs.request_ok()
		).post(context.transfer)
		return response

	def transfer_invalid(self, context: TransferTestContext):
		auth = context.user_auth
		response = CrudRequester(
				RequestSpecs.auth_headers(username=auth.username, password=auth.password),
				Endpoint.TRANSFER,
				ResponseSpecs.request_unprocessable_entity()
		).post(context.transfer)
		return response

	def credit_requesting(self, context: CreditRequestingContext):
		response = ValidatedCrudRequester(
				RequestSpecs.auth_headers(username=context.user.username, password=context.user.password),
				Endpoint.CREDIT_REQUEST,
				ResponseSpecs.request_created()
		).post(context.credit)
		return response

	def credit_requesting_invalid(self, context: CreditRequestingContext):
		response = CrudRequester(
				RequestSpecs.auth_headers(username=context.user.username, password=context.user.password),
				Endpoint.CREDIT_REQUEST,
				ResponseSpecs.request_not_found()
		).post(context.credit)
		return response

	def credit_repay(self, context: CreditRepayContext):
		response = ValidatedCrudRequester(
				RequestSpecs.auth_headers(username=context.user.username, password=context.user.password),
				Endpoint.CREDIT_REPAY,
				ResponseSpecs.request_ok()
		).post(context.repay)
		return response

	def credit_repay_invalid(self, context: CreditRepayContext):
		response = CrudRequester(
				RequestSpecs.auth_headers(username=context.user.username, password=context.user.password),
				Endpoint.CREDIT_REPAY,
				ResponseSpecs.request_unprocessable_entity()
		).post(context.repay)
		return response
