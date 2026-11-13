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
  if (current_user_get('deposit_used', 0.0)+amount)>daily_deposit_limit:
       print("Deposit declined")
       return
  current_user['balance'] += amount
  current_user['deposit used']=current_user_get('deposit_used', 0.0) + amount
  atm_data['cash_reserve'] += amount
  print(f"Deposited successfully: {amount:.2f} AZN")
  print(f"New balance: {current_user['balance']:.2f} AZN")
  def withdraw_money(current_user , atm_data)
  try:
      amount=float(input("Enter amount to withdraw (AZN): "))
  except ValueError:
      print("Invalid input. Please enter a valid number.")
      return
  if amount<=0:
      print("Withdrawal declined: amount must be positive.")
  if amount>atm_data['cash_reserve']:
      return
      print("Withdrawal declined")
      return
  daily_withdrawal_limit=1000.00
  if (current_user_get('withdrawal_used'), 0.0+amount)>daily_withdrawal_limit:
      print("Withdrawal declined")
      return
  commission=0.0
  if amount>500:
      comission=(amount-500)*0.02
  total_deduction=amount+commission
  if total_deduction>current_user['balance']:
      print("Withdrawal declined:Insufficient balance.")
      return
  current_user['balance'] -= total_deduction
  current_user['withdrawal-used']=current_user_get('withdrawal_used', 0.0) + amount
  atm_data['cash_reserve'] -= amount
  print(f"Withdrawal successful: {amount:.2f} AZN")
  if commission > 0:
      print(f"Commission applied: {commission:.2f} AZN")
print(f"New balance: {current_user['balance']:.2f} AZN")
def show_daily_limits(current_user):
    print("--- Daily Limits ---")
    deposit_used = current_user.get('deposit_used', 0.0)
    deposit_remaining = 2000.00 - deposit_used
    print(f"Deposit Used Today: {deposit_used:.2f} AZN (Limit: 2000.00 AZN)")
    print(f"Remaining Deposit Limit: {deposit_remaining:.2f} AZN")
    
    print("-" * 25)
    withdrawal_used = current_user.get('withdrawal_used', 0.0)
    withdrawal_remaining = 1000.00 - withdrawal_used
    print(f"Withdrawal Used Today: {withdrawal_used:.2f} AZN (Limit: 1000.00 AZN)")
    print(f"Remaining Withdrawal Limit: {withdrawal_remaining:.2f} AZN")





                     
      
