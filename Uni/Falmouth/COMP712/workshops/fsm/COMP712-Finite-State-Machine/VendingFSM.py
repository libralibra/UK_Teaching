from enum import Enum, auto

class VendingMachineState(Enum):
    START = auto()
    ACCEPTING_COINS = auto()
    DISPENSE_COCA = auto()

class VendingMachine:
    def __init__(self):
        self.state = VendingMachineState.START
        self.balance = 0.0
        self.can_price = 2.5

    def insert_coin(self, value):
        if self.state == VendingMachineState.ACCEPTING_COINS or self.state == VendingMachineState.START:
            self.state = VendingMachineState.ACCEPTING_COINS
            self.balance += value
            print(f"Inserted £{value} coin. Current balance: £{self.balance}")
        else:
            print("Invalid state for coin insertion. Try again after dispensing Coca.")

    def dispense_coca(self):
        if self.state == VendingMachineState.ACCEPTING_COINS:
            if self.balance >= self.can_price:
                self.state = VendingMachineState.DISPENSE_COCA
                change = self.balance - self.can_price
                print(f"Coca dispensed! Your change: £{change}")
                self.balance = 0.0
            else:
                print("Insufficient balance. Please insert more coins.")
        else:
            print("Invalid state for dispensing Coca. Insert a coin first.")
        self.state = VendingMachineState.ACCEPTING_COINS    

# Example usage:
vending_machine = VendingMachine()

while True:
    print("Available commands:")
    print("1. insert_coin <value>")
    print("2. dispense_coca")
    print("3. exit")

    user_input = input("Enter your command: ")

    if user_input.lower() == 'exit':
        break

    command_parts = user_input.split()
    if command_parts[0] == 'insert_coin':
        if len(command_parts) == 2:
            value = float(command_parts[1])
            vending_machine.insert_coin(value)
        else:
            print("Invalid command. Example: insert_coin 1")
    elif command_parts[0] == 'dispense_coca':
        vending_machine.dispense_coca()
    else:
        print("Invalid command. Please choose a valid command from the menu.")
