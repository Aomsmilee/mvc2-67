import json
import os
import datetime

class InventoryModel:
    def __init__(self, filename="inventory.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    # แปลง expiration_date กลับเป็น date object
                    for product in data.get("products", []):
                        if "expiration_date" in product:
                            product["expiration_date"] = datetime.datetime.strptime(product["expiration_date"], "%Y-%m-%d").date()
                    for product in data.get("rejected_products", []):
                        if "expiration_date" in product:
                            product["expiration_date"] = datetime.datetime.strptime(product["expiration_date"], "%Y-%m-%d").date()
                    return data
            except json.JSONDecodeError:
                print("Error reading the JSON file. Using default data.")
                return {"products": [], "rejected_products": []}  # ใช้ข้อมูลเริ่มต้นแทน
        else:
            return {"products": [], "rejected_products": []}  # ถ้าไฟล์ไม่พบ, สร้างข้อมูลเริ่มต้น

    def save_data(self):
        # แปลง expiration_date เป็น string ก่อนบันทึก
        for product in self.data["products"]:
            if isinstance(product.get("expiration_date"), datetime.date):
                product["expiration_date"] = product["expiration_date"].strftime("%Y-%m-%d")
        
        for product in self.data["rejected_products"]:
            if isinstance(product.get("expiration_date"), datetime.date):
                product["expiration_date"] = product["expiration_date"].strftime("%Y-%m-%d")
        
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def add_product(self, product):
        # ถ้าสินค้าถูกปฏิเสธ ให้นำไปเก็บใน rejected_products
        if "rejected" in product and product["rejected"]:
            self.data["rejected_products"].append(product)
        else:
            self.data["products"].append(product)
        self.save_data()

    def product_exists(self, product_id):
        return any(p["id"] == product_id for p in self.data["products"])
