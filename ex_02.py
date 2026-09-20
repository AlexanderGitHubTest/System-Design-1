"""
Класс BankAccount:
Приватное поле balance (баланс), типа double.
Конструктор, который принимает начальное значение баланса.
Метод deposit, который принимает сумму для депозита и увеличивает баланс.
Метод withdraw, который принимает сумму для снятия и уменьшает баланс.
Метод getBalance, который возвращает текущий баланс.

Убедитесь, что:
В методе deposit и методе withdraw нет проверки на отрицательную сумму.
В методе withdraw баланс может стать отрицательным.

Напишите тестовый класс, в котором создаётся объект BankAccount, выполняются различные операции и выводится результат баланса.
"""


class BankAccount:

    def __init__(self, initial_balance: float) -> None:
        if not isinstance(initial_balance, float):
            self._error = True
            return
        self._error = False
        self._balance = initial_balance

    def deposit(self, amount: float) -> None:
        if not isinstance(amount, float):
            self._error = True
            return
        if self._error:
            return        
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if not isinstance(amount, float):
            self._error = True
            return
        if self._error:
            return        
        self._balance -= amount

    def get_balance(self) -> float:
        if self._error:
            return "Incorrect account balance!"
        return self._balance


class TestBankAccount:
    
    def __init__(
        self, 
        initial_amount: float,
        deposit_amount: float,
        withdraw_amount: float
    ) -> None:
        self.bank_account = BankAccount(initial_amount)
        self.bank_account.deposit(deposit_amount)
        self.bank_account.withdraw(withdraw_amount)

    def get_account_balance(self) -> float:
        return self.bank_account.get_balance()
      

def main():
    test_bank_account = TestBankAccount(300.5, 15.3, 10.4)
    print(test_bank_account.get_account_balance()) # 305.4
    test_bank_account = TestBankAccount(0.5, 15.3, 10.4)
    print(test_bank_account.get_account_balance()) # 5.4
    test_bank_account = TestBankAccount(0.5, 15.3, 100.4)
    print(test_bank_account.get_account_balance()) # -84.6
    test_bank_account = TestBankAccount(0.5, "ff", 100.4)
    print(test_bank_account.get_account_balance()) # "Incorrect account balance!"


if __name__ == "__main__":
    main()
