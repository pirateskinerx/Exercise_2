from datetime import datetime
from typing import List, Dict, Optional

class BankAccount:
    """
    คลาส BankAccount สำหรับจัดการบัญชีธนาคาร
    ใช้หลักการ Encapsulation เพื่อป้องกันการเข้าถึงข้อมูลโดยตรง
    """
    
    # Class variable สำหรับเก็บจำนวนบัญชีทั้งหมดในระบบ
    __total_accounts = 0
    
    def __init__(self, account_number: int, balance: float, name: str):
        """
        Constructor สำหรับสร้างบัญชีใหม่
        
        Args:
            account_number (int): หมายเลขบัญชี
            balance (float): ยอดเงินเริ่มต้น
            name (str): ชื่อเจ้าของบัญชี
        """
        # Private attributes
        self.__account_number = account_number
        self.__balance = balance
        self.__name = name
        self.__transaction_history: List[Dict] = []  # เก็บประวัติการทำรายการ
        self.__account_status = "active"  # สถานะบัญชี
        self.__created_at = datetime.now()
        
        # เพิ่มจำนวนบัญชีในระบบ
        BankAccount.__total_accounts += 1

    def __str__(self) -> str:
        """แสดงข้อมูลบัญชีในรูปแบบที่อ่านง่าย"""
        return f"Account Number: {self.__account_number}, Balance: {self.__balance:,.2f} บาท, Name: {self.__name}"

    def deposit(self, amount: float) -> None:
        """
        ฝากเงินเข้าบัญชี
        
        Args:
            amount (float): จำนวนเงินที่ต้องการฝาก
            
        Raises:
            ValueError: ถ้าจำนวนเงินไม่ถูกต้องหรือบัญชีถูกระงับ
        """
        if self.__account_status != "active":
            raise ValueError("ไม่สามารถทำรายการได้ เนื่องจากบัญชีถูกระงับ")
        
        if amount <= 0:
            raise ValueError("จำนวนเงินฝากต้องมากกว่า 0")
        
        self.__balance += amount
        self.__add_transaction("deposit", amount)

    def withdraw(self, amount: float) -> None:
        """
        ถอนเงินจากบัญชี
        
        Args:
            amount (float): จำนวนเงินที่ต้องการถอน
            
        Raises:
            ValueError: ถ้าจำนวนเงินไม่ถูกต้อง, เงินไม่พอ, หรือบัญชีถูกระงับ
        """
        if self.__account_status != "active":
            raise ValueError("ไม่สามารถทำรายการได้ เนื่องจากบัญชีถูกระงับ")
        
        if amount <= 0:
            raise ValueError("จำนวนเงินถอนต้องมากกว่า 0")
        
        if self.__balance < amount:
            raise ValueError("ยอดเงินในบัญชีไม่เพียงพอ")
        
        self.__balance -= amount
        self.__add_transaction("withdraw", amount)

    def get_balance(self) -> float:
        """ดึงข้อมูลยอดเงินคงเหลือในบัญชี"""
        return self.__balance

    def get_transaction_history(self) -> List[Dict]:
        """ดึงประวัติการทำรายการทั้งหมด"""
        return self.__transaction_history.copy()

    def suspend_account(self) -> None:
        """ระงับการใช้งานบัญชี"""
        self.__account_status = "suspended"

    def activate_account(self) -> None:
        """เปิดใช้งานบัญชี"""
        self.__account_status = "active"

    def __add_transaction(self, transaction_type: str, amount: float) -> None:
        """
        เพิ่มประวัติการทำรายการ (Private method)
        
        Args:
            transaction_type (str): ประเภทการทำรายการ (deposit/withdraw)
            amount (float): จำนวนเงิน
        """
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now(),
            "balance_after": self.__balance
        }
        self.__transaction_history.append(transaction)

    @classmethod
    def get_total_accounts(cls) -> int:
        """ดึงจำนวนบัญชีทั้งหมดในระบบ"""
        return cls.__total_accounts

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    try:
        # สร้างบัญชีใหม่
        account = BankAccount(1001, 1000.0, "สมชาย")
        
        print("=== ข้อมูลบัญชีเริ่มต้น ===")
        print(account)
        
        # ทดสอบการฝากเงิน
        account.deposit(500.0)
        print("\n=== หลังจากฝากเงิน 500 บาท ===")
        print(f"ยอดเงินคงเหลือ: {account.get_balance():,.2f} บาท")
        
        # ทดสอบการถอนเงิน
        account.withdraw(300.0)
        print("\n=== หลังจากถอนเงิน 300 บาท ===")
        print(f"ยอดเงินคงเหลือ: {account.get_balance():,.2f} บาท")
        
        # แสดงประวัติการทำรายการ
        print("\n=== ประวัติการทำรายการ ===")
        for transaction in account.get_transaction_history():
            print(f"ประเภท: {transaction['type']}")
            print(f"จำนวนเงิน: {transaction['amount']:,.2f} บาท")
            print(f"เวลา: {transaction['timestamp']}")
            print(f"ยอดคงเหลือ: {transaction['balance_after']:,.2f} บาท")
            print("-" * 30)
        
        # ทดสอบการระงับบัญชี
        print("\n=== ทดสอบการระงับบัญชี ===")
        account.suspend_account()
        try:
            account.deposit(100.0)
        except ValueError as e:
            print(f"ทดสอบฝากเงินหลังระงับบัญชี: {e}")
        
        # แสดงจำนวนบัญชีทั้งหมดในระบบ
        print(f"\nจำนวนบัญชีทั้งหมดในระบบ: {BankAccount.get_total_accounts()}")
        
    except ValueError as e:
        print(f"เกิดข้อผิดพลาด: {e}") 