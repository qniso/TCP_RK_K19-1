import threading

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.lock = threading.Lock() # ініціалізація монітора

    def deposit(self, amount):
        with self.lock: # заблокувати монітор
            self.balance += amount # збільшити баланс

    def withdraw(self, amount):
        with self.lock: # заблокувати монітор
            if self.balance >= amount:
                self.balance -= amount # зменшити баланс
                return True
            else:
                return False

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
    t = threading.Thread(target=account_holder, args=(account, f"Людина {i}", "withdraw", 25))
    threads.append(t)
    t = threading.Thread(target=account_holder, args=(account, f"Людина {i}", "deposit", 10))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Остаточний баланс рахунку: $", account.balance) # вивести остаточний баланс на рахунку