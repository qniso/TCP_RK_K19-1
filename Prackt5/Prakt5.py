import threading

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.semaphore = threading.Semaphore() # ініціалізація семафора
        self.deposit_semaphore = threading.Semaphore() # ініціалізація семафора для депозитів

    def deposit(self, amount):
        self.deposit_semaphore.acquire() # заблокувати семафор для депозитів
        self.semaphore.acquire() # заблокувати семафор
        self.balance += amount # збільшити баланс
        self.semaphore.release() # розблокувати семафор

    def withdraw(self, amount):
        while True:
            self.semaphore.acquire() # заблокувати семафор
            if self.balance >= amount:
                self.balance -= amount # зменшити баланс
                self.semaphore.release() # розблокувати семафор
                self.deposit_semaphore.release() # розблокувати семафор для депозитів
                return True
            self.semaphore.release() # розблокувати семафор
            # Чекаємо на здійснення депозиту
            self.deposit_semaphore.acquire() 

# Приклад використання
def account_holder(account, name, action, amount):
    if action == "deposit":
        account.deposit(amount)
        print("{} поклала ${}".format(name, amount))
    elif action == "withdraw":
        success = account.withdraw(amount)
        if success:
            print("{} зняла ${}".format(name, amount))
        else:
            print("{} не змогла зняти ${}".format(name, amount))

account = BankAccount(100)
threads = []
for i in range(5):
    t = threading.Thread(target=account_holder, args=(account, f" Людина {i}", "withdraw", 25))
    threads.append(t)
    t = threading.Thread(target=account_holder, args=(account, f" Людина {i}", "deposit", 10))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Остаточний баланс рахунку: $", account.balance) # вивести остаточний баланс на рахунку