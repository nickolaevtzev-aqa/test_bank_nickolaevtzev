from sqlalchemy.orm import Session

from src.main.api.db.models.credit_table import CreditTable


class CreditCrudDb:
	@staticmethod
	def get_credit_by_account_id(db: Session, account_id: int) -> CreditTable | None:
		return db.query(CreditTable).filter_by(account_id=account_id).first()

