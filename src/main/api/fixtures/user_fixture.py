import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_requesting_request import CreditRequestingRequest
from src.main.api.models.custom_models_for_fixtures import DepositTestContext, TransferTestContext, \
	CreditRequestingContext, CreditRepayContext
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.fixture
def create_user_request(api_manager):
	user_request = RandomModelGenerator.generate(CreateUserRequest)
	user_request.role = "ROLE_USER"
	api_manager.admin_steps.create_user(user_request)
	return user_request


@pytest.fixture
def create_user_credit_request(api_manager):
	user_request = RandomModelGenerator.generate(CreateUserRequest)
	user_request.role = "ROLE_CREDIT_SECRET"
	api_manager.admin_steps.create_user(user_request)
	return user_request


@pytest.fixture
def deposit_request_fixture(api_manager):
	user_request = RandomModelGenerator.generate(CreateUserRequest)
	user_request.role = "ROLE_USER"
	user_auth = api_manager.admin_steps.create_user(user_request)
	user_auth.password = user_request.password  # Подменяем хешированный пароль корректным паролем

	account_info = api_manager.user_steps.create_account(user_auth)
	deposit_request = RandomModelGenerator.generate(DepositRequest)
	deposit_request.accountId = account_info.id  # Принудительно связываем сгенерированный запрос с созданным accountId
	return DepositTestContext(
			user=user_auth,
			deposit=deposit_request
	)


@pytest.fixture
def transfer_request_fixture(api_manager):
	# Создаем пользователя
	user_request = RandomModelGenerator.generate(CreateUserRequest)
	user_request.role = "ROLE_USER"
	user_auth = api_manager.admin_steps.create_user(user_request)
	user_auth.password = user_request.password

	# Создаем ему два счёта
	first_acc = api_manager.user_steps.create_account(user_auth)
	second_acc = api_manager.user_steps.create_account(user_auth)

	# Депозитим 1000 на первый счет
	deposit_req = DepositRequest(accountId=first_acc.id, amount=1000.0)
	temp_deposit = DepositTestContext(user=user_auth, deposit=deposit_req)
	api_manager.user_steps.deposit(temp_deposit)

	# Формируем запрос на перевод 500
	transfer_req = TransferRequest(
			fromAccountId=first_acc.id,
			toAccountId=second_acc.id,
			amount=500.0
	)

	return TransferTestContext(
			user_auth=user_auth,
			from_account=first_acc,
			to_account=second_acc,
			transfer=transfer_req
	)


@pytest.fixture
def credit_requesting_fixture(api_manager):
	# Создаем пользователя
	user_request = RandomModelGenerator.generate(CreateUserRequest)
	user_request.role = "ROLE_CREDIT_SECRET"
	user_auth = api_manager.admin_steps.create_user(user_request)
	user_auth.password = user_request.password

	account_info = api_manager.user_steps.create_account(user_auth)
	credit_request = RandomModelGenerator.generate(CreditRequestingRequest)
	credit_request.accountId = account_info.id  # Принудительно связываем сгенерированный запрос с созданным accountId

	return CreditRequestingContext(
			user=user_auth,
			credit=credit_request
	)


@pytest.fixture
def credit_repay_fixture(api_manager):
	# 1. Создаем пользователя
	user_req = RandomModelGenerator.generate(CreateUserRequest)
	user_req.role = "ROLE_CREDIT_SECRET"
	user_auth = api_manager.admin_steps.create_user(user_req)
	user_auth.password = user_req.password

	# 2. Создаем ему счет
	account_info = api_manager.user_steps.create_account(user_auth)

	# 3. Запрашиваем кредит на этот счет
	credit_req = RandomModelGenerator.generate(CreditRequestingRequest)
	credit_req.accountId = account_info.id  # Связываем со счетом

	# Отправляем запрос на кредит
	temp_credit_context = CreditRequestingContext(user=user_auth, credit=credit_req)
	credit_response = api_manager.user_steps.credit_requesting(temp_credit_context)

	# 4. Формируем запрос на погашение
	repay_req = CreditRepayRequest(
			creditId=credit_response.creditId,  # Реальный ID одобренного кредита
			accountId=account_info.id,  # Реальный ID созданного счета пользователя!
			amount=credit_response.amount  # Сумма строго равна сумме кредита
	)

	return CreditRepayContext(
			user=user_auth,
			repay=repay_req
	)

