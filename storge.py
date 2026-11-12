import json
import os
from datetime import datetime

DB_FILE = "database.json"

def load_database():
    if not os.path.exists(DB_FILE):
        default_data = {
            "atm_cash": 5000.00,
            "users": {
                "user01": {
                    "account_number": "10010001",
                    "password_hash": "Test@123",
                    "balance": 2500.00,
                    "status": "Active",
                    "failed_attempts": 0,
                    "lockout_expiry": None,
                    "daily_deposit_total": 0.0,
                    "deposit_date": datetime.now().strftime("%Y-%m-%d"),
                    "daily_transfer_count": 0,
                    "transfer_date": datetime.now().strftime("%Y-%m-%d"),
                    "transaction_history": []
                },
                "user02": {
                    "account_number": "10010002",
                    "password_hash": "Test@456",
                    "balance": 1500.00,
                    "status": "Active",
                    "failed_attempts": 0,
                    "lockout_expiry": None,
                    "daily_deposit_total": 0.0,
                    "deposit_date": datetime.now().strftime("%Y-%m-%d"),
                    "daily_transfer_count": 0,
                    "transfer_date": datetime.now().strftime("%Y-%m-%d"),
                    "transaction_history": []
                },
                "user03": {
                    "account_number": "10010003",
                    "password_hash": "Test@789",
                    "balance": 3000.00,
                    "status": "Active",
                    "failed_attempts": 0,
                    "lockout_expiry": None,
                    "daily_deposit_total": 0.0,
                    "deposit_date": datetime.now().strftime("%Y-%m-%d"),
                    "daily_transfer_count": 0,
                    "transfer_date": datetime.now().strftime("%Y-%m-%d"),
                    "transaction_history": []
                }
            }
        }
        save_database(default_data)
        return default_data
    
    with open(DB_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_database(data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def check_and_reset_daily_limits(user_data):
    current_date = datetime.now().strftime("%Y-%m-%d")
    if user_data.get("transfer_date") != current_date:
        user_data["daily_transfer_count"] = 0
        user_data["transfer_date"] = current_date

def make_transfer(sender_username, sender_data, db_users):
    check_and_reset_daily_limits(sender_data)
    
    if sender_data["daily_transfer_count"] >= 5:
        print("Transfer rejected: You have exceeded the daily limit of 5 transfers.")
        return False
        
    recipient_acc = input("Enter the recipient's account number: ")
    
    if recipient_acc == sender_data["account_number"]:
        print("Error: You cannot transfer money to your own account.")
        return False
        
    recipient_username = None
    recipient_data = None
    for uname, udata in db_users.items():
        if udata["account_number"] == recipient_acc:
            recipient_username = uname
            recipient_data = udata
            break
            
    if not recipient_data:
        print("Error: Such account number does not exist.")
        return False
        
    try:
        amount = float(input("Enter the amount you want to transfer (AZN): "))
    except ValueError:
        print("Invalid amount entered.")
        return False
        
    if amount <= 0:
        print("Amount must be positive.")
        return False
        
    if sender_data["balance"] < amount:
        print("Insufficient funds in your balance.")
        return False
        
    confirm = input(f"Do you confirm the transfer? ({amount} AZN) [Y/N]: ")
    if confirm.upper() != 'Y':
        print("Transfer cancelled.")
        return False
        
    sender_balance_before = sender_data["balance"]
    recipient_balance_before = recipient_data["balance"]
    
    sender_data["balance"] -= amount
    recipient_data["balance"] += amount
    sender_data["daily_transfer_count"] += 1
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    s_txn_id = f"TXN{len(sender_data['transaction_history']) + 1:04d}"
    sender_data["transaction_history"].append({
        "id": s_txn_id,
        "date_time": now_str,
        "type": "Transfer Sent",
        "amount": amount,
        "balance_before": sender_balance_before,
        "balance_after": sender_data["balance"],
        "fee": 0.0,
        "recipient_account": recipient_acc
    })
    
    r_txn_id = f"TXN{len(recipient_data['transaction_history']) + 1:04d}"
    recipient_data["transaction_history"].append({
        "id": r_txn_id,
        "date_time": now_str,
        "type": "Transfer Received",
        "amount": amount,
        "balance_before": recipient_balance_before,
        "balance_after": recipient_data["balance"],
        "fee": 0.0,
        "recipient_account": sender_data["account_number"]
    })
    
    print("Transfer completed successfully!")
    return True

def show_transaction_history(user_data):
    history = user_data.get("transaction_history", [])
    if not history:
        print("No transaction history available.")
        return
        
    print("\n--- RECENT TRANSACTIONS ---")
    for txn in history[-10:]:
        print(f"ID: {txn['id']}")
        print(f"Date: {txn['date_time']}")
        print(f"Type: {txn['type']}")
        print(f"Amount: {txn['amount']:.2f} AZN")
        print(f"Previous Balance: {txn['balance_before']:.2f} AZN")
        print(f"New Balance: {txn['balance_after']:.2f} AZN")
        if txn.get('recipient_account'):
            print(f"Account / Counterparty: {txn['recipient_account']}")
        print("-" * 30)