import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.custom_models_for_fixtures import CreditRepayContext


@pytest.mark.api
class TestCreditRepay:
	def test_credit_repay(self, db_session: Session, api_manager: ApiManager, credit_repay_fixture: CreditRepayContext):
		response = api_manager.user_steps.credit_repay(credit_repay_fixture)
		assert credit_repay_fixture.repay.amount == response.amountDeposited

		credit_repay_from_db = TransactionCrudDb.get_transaction_by_from_account_id(
				db_session,
				credit_repay_fixture.repay.accountId
		)

		assert credit_repay_from_db is not None
		assert credit_repay_from_db.from_account_id == credit_repay_fixture.repay.accountId

	def test_credit_repay_invalid_amount_exceeds_remaining(self, db_session: Session, api_manager: ApiManager,
	                                                       credit_repay_fixture: CreditRepayContext):
		credit_repay_fixture.repay.amount -= 1
		api_manager.user_steps.credit_repay_invalid(credit_repay_fixture)

		credit_repay_from_db = TransactionCrudDb.get_transaction_by_from_account_id(
				db_session,
				credit_repay_fixture.repay.accountId
		)

		assert credit_repay_from_db is None
