from backend.core.config import ENVIRONMENT
from backend.core.helpers.constants import EnvironmentEnum

from .cashback.vendor import CashbackClient, ExternalCashbackClient, NoneCashbackClient

DefaultCashbackClient = NoneCashbackClient if ENVIRONMENT == EnvironmentEnum.testing else ExternalCashbackClient
