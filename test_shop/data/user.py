import uuid
from dataclasses import dataclass, replace


@dataclass
class UserData:
    first_name: str = "Ivan"
    last_name: str = "Petrov"
    address: str = "Lenina 1"
    city: str = "Moscow"
    state: str = "Moscow"
    zip_code: str = "101000"
    phone: str = "+79991234567"
    ssn: str = "123-45-6789"
    username: str = ""
    password: str = "Passw0rd!"
    confirm: str = "Passw0rd!"

    @classmethod
    def random(cls, **overrides) -> "UserData":
        """Пользователь с уникальным логином; любые поля можно переопределить."""
        base = cls(username=f"user_{uuid.uuid4().hex[:10]}")
        return replace(base, **overrides)
