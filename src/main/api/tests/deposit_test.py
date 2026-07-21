from http import HTTPStatus

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.custom_models_for_fixtures import DepositTestContext


@pytest.mark.api
class TestDeposit:
	def test_deposit(self, db_session: Session, api_manager: ApiManager, deposit_request_fixture: DepositTestContext):
		response = api_manager.user_steps.deposit(deposit_request_fixture)
		assert deposit_request_fixture.deposit.amount == response.balance

		deposit_from_db = TransactionCrudDb.get_transaction_by_to_account_id(db_session, response.id)

		assert deposit_from_db.to_account_id == response.id, 'Перевод не найден'

	@pytest.mark.parametrize(
			"edge_amount",
			[999, 9001]
	)
	def test_deposit_invalid_edge_value(self, db_session: Session, api_manager: ApiManager,
	                                    deposit_request_fixture: DepositTestContext, edge_amount: int):
		deposit_request_fixture.deposit.amount = edge_amount
		api_manager.user_steps.deposit_invalid(deposit_request_fixture)

		deposit_from_db = TransactionCrudDb.get_transaction_by_to_account_id(
				db_session,
				deposit_request_fixture.deposit.accountId
		)

		assert deposit_from_db is None
