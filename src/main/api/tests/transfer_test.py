import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.custom_models_for_fixtures import TransferTestContext


@pytest.mark.api
class TestTransfer:
	def test_transfer(self, db_session: Session, api_manager: ApiManager, transfer_request_fixture: TransferTestContext):
		response = api_manager.user_steps.transfer(transfer_request_fixture)

		assert transfer_request_fixture.transfer.amount == response.fromAccountIdBalance

		transfer_from_db = TransactionCrudDb.get_transaction_by_to_account_id(db_session, response.toAccountId)

		assert transfer_from_db.to_account_id == response.toAccountId

	@pytest.mark.parametrize(
			"invalid_amount", 2000.0
	)
	def test_transfer_invalid(self, db_session: Session,  api_manager: ApiManager,
	                          transfer_request_fixture: TransferTestContext, invalid_amount: float):
		transfer_request_fixture.transfer.amount = invalid_amount

		api_manager.user_steps.transfer_invalid(transfer_request_fixture)

		transfer_from_db = TransactionCrudDb.get_transaction_by_to_account_id(
				db_session,
				transfer_request_fixture.transfer.toAccountId
		)

		assert transfer_from_db is None
