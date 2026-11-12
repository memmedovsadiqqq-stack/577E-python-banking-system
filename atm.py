def view_account_info(current_user):
    print("--- Account Information ---")
    print(f"Account Holder: {current_user['username']}")
    print(f"Account Number: {current_user['account_number']}")
    print(f"Available Balance: {current_user['balance']:.2f} AZN")
    print(f"Account Status: {current_user['status']}")
def deposit_money(current_user, atm_data):
try:
  amount=float(input("Enter amount to deposit (AZN: "))
  except ValueError:
  print("Invalid input. Please enter a valid number.")
  return
  if amount<=0:
       print("deposit declined: amount must be positive")
  return
  daily_deposit_limit=2000.00
  if amount>daily_deposit_limit:
       print("Deposit declined")
       return
  current_user['balance'] += amount
    print(f"Deposited successfully: {amount:.2f} AZN")
    print(f"New balance: {current_user['balance']:.2f} AZN")

      
