from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import TransactionTable


class TransactionCrudDb:
	@staticmethod
	def get_transaction_by_to_account_id(db: Session, to_account_id: int) -> TransactionTable | None:
		return db.query(TransactionTable).filter_by(to_account_id=to_account_id).first()

	@staticmethod
	def get_transaction_by_from_account_id(db: Session, from_account_id: int) -> TransactionTable | None:
		return db.query(TransactionTable).filter_by(from_account_id=from_account_id).first()
	