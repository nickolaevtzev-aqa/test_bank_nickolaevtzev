import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.custom_models_for_fixtures import CreditRequestingContext


@pytest.mark.api
class TestCreditRequest:
	def test_credit(self, db_session: Session, api_manager: ApiManager,
	                credit_requesting_fixture: CreditRequestingContext):
		response = api_manager.user_steps.credit_requesting(credit_requesting_fixture)

		assert credit_requesting_fixture.credit.amount == response.amount

		credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, response.id)

		assert credit_from_db.account_id == response.id

	def test_credit_request_invalid_id(self, db_session: Session, api_manager: ApiManager,
	                                   credit_requesting_fixture: CreditRequestingContext):
		credit_requesting_fixture.credit.accountId += 1
		api_manager.user_steps.credit_requesting_invalid(credit_requesting_fixture)

		credit_from_db = CreditCrudDb.get_credit_by_account_id(
				db_session,
				credit_requesting_fixture.credit.accountId
		)

		assert credit_from_db is None

