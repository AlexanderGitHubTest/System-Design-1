"""
Класс BankAccount:
Приватное поле balance (баланс), типа double.
Конструктор, который принимает начальное значение баланса.
Метод deposit, который принимает сумму для депозита и увеличивает баланс.
Метод withdraw, который принимает сумму для снятия и уменьшает баланс.
Метод getBalance, который возвращает текущий баланс.

Добавлены проверки:
- В методе deposit проверка на отрицательные суммы, чтобы нельзя было уменьшить баланс путем депозита отрицательного значения.
- В методе withdraw проверка на отрицательные суммы, чтобы нельзя было увеличить баланс путем попытки снятия отрицательного значения.
- В методе withdraw проверка на достаточность средств на счете, что не позволяет уйти в отрицательный баланс банковского счета. 

Добавлен тестовый класс, в котором создаётся объект BankAccount, выполняются различные операции и выводится результат баланса.
"""

class NoneClass:
    pass

void = NoneClass()


class BankAccount:

    # Константы для статуса после конструктора
    INIT_OK: int = 0 # В конструктор передано корректное значение
    INIT_ERR_NEGATIVE: int = 1 # В конструктор передано отрицательное значение

    # Константы для статуса после добавления суммы на счёт
    DEPOSIT_NILL: int = 0 # Операция добавления на счёт ещё не выполнялась
    DEPOSIT_OK: int = 1 # Для добавления на счет передано корректное значение
    DEPOSIT_ERR_NEGATIVE: int = 2 # Для добавления на счет  передано отрицательное значение

    # Константы для статуса после снятия суммы со счёта
    WITHDRAW_NIL: int = 0 # Операция снятия суммы со счёта ещё не выполнялась
    WITHDRAW_OK: int = 1 # Для операция снятия суммы со счёта передано корректное значение
    WITHDRAW_ERR_NEGATIVE: int = 2 # Для операция снятия суммы со счёта передано 
                                   # отрицательное значение
    WITHDRAW_ERR_NOT_ENOUGH_FUNDS: int = 3 # Не хватает денег на счёте

    def __init__(self, initial_balance: float) -> None:
        self._deposit_status = 0
        self._withdraw_status = 0
        if initial_balance < 0.0:
            self._init_status = 1
            self._balance = void
            return
        self._init_status = 0
        self._balance = initial_balance

    def deposit(self, amount: float) -> None:
        assert self._balance != void, ("Некорретный начальный баланс "
                                       + "- вносить средства запрещено!"
        )
        if amount < 0.0:
            self._deposit_status = 2
            return
        self._deposit_status = 1
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        assert self._balance != void, ("Некорретный начальный баланс "
                                       + "- снимать средства запрещено!"
        )
        if amount < 0.0:
            self._withdraw_status = 2
            return
        if amount > self._balance:
            self._withdraw_status = 3
            return
        self._withdraw_status = 1
        self._balance -= amount

    def get_balance(self) -> float|NoneClass:
        return self._balance

    def get_init_status(self) -> int:
        return self._init_status

    def get_deposit_status(self) -> int:
        return self._deposit_status

    def get_withdraw_status(self) -> int:
        return self._withdraw_status


class TestBankAccount:

    def __init__(self) -> None:

        account: BankAccount = BankAccount(1000)
        # Баланс 1000, статус выполнения команды 0 (INIT_OK)
        print(f"Начальный баланс: "
              + f"{account.get_balance()} "
              + f"(статус команды {account.get_init_status()})"
        )
        
        account.deposit(500) # Баланс 1500, статус выполнения команды 1 (DEPOSIT_OK)
        print(f"Баланс после депозита 500: "
              + f"{account.get_balance()} "
              + f"(статус команды {account.get_deposit_status()})"
        )
        
        account.withdraw(200) # Баланс 1300, статус выполнения команды 1 (WITHDRAW_OK)
        print(f"Баланс после снятия 200: "
              + f"{account.get_balance()} "
              + f"(статус команды {account.get_withdraw_status()})"
        )
        
        account.withdraw(2000) # Баланс 1300, статус выполнения команды 3
                               # (WITHDRAW_ERR_NOT_ENOUGH_FUNDS)
        print(f"Баланс после снятия 2000: "
              + f"{account.get_balance()} "
              + f"(статус команды {account.get_withdraw_status()})"
        )
        
        account.deposit(-100) # Некорректный депозит
                              # Баланс 1300, статус выполнения команды 2
                              # (DEPOSIT_ERR_NEGATIVE)
        print(f"Баланс после некорректного депозита -100: "
              + f"{account.get_balance()} "
              + f"(статус команды {account.get_deposit_status()})"
        )
        
        account.withdraw(-50) # Некорректное снятие
                              # Баланс 1300, статус выполнения команды 2
                              # (WITHDRAW_ERR_NEGATIVE)
        print(f"Баланс после некорректного снятия -50: "
              + f"{account.get_balance()} "
              + f"(статус команды {account.get_withdraw_status()})"
        )

        account = BankAccount(-1000)
        # Баланс void (значение NIL), статус выполнения команды 1 (INIT_ERR_NEGATIVE)
        print(f"Начальный баланс: "
              + f"{account.get_balance()} "
              + f"(статус команды {account.get_init_status()})"
        )

        account.deposit(100) # Будет AssertionError


def main():
    TestBankAccount()


if __name__ == "__main__":
    main()
