from inventory_model import InventoryModel
from inventory_view import InventoryView
import datetime

class InventoryController:
    def __init__(self):
        self.model = InventoryModel()
        self.view = InventoryView(self)

        # เพิ่มการเรียก on_type_selected เมื่อมีการเปลี่ยนแปลงประเภทสินค้า
        self.view.type_menu.bind("<<ComboboxSelected>>", self.on_type_selected)

        # ตัวแปรเก็บจำนวนสินค้าที่รับเข้าและปฏิเสธในแต่ละประเภท
        self.accepted = {"อาหาร": 0, "อิเล็กทรอนิกส์": 0, "เสื้อผ้า": 0}
        self.rejected = {"อาหาร": 0, "อิเล็กทรอนิกส์": 0, "เสื้อผ้า": 0}

    def add_product(self):
        product_id, product_type = self.view.get_product_info()

        # ตรวจสอบว่าผู้ใช้กรอกรหัสสินค้าหรือไม่
        if not product_id:
            self.view.show_message("ข้อผิดพลาด", "กรุณากรอกรหัสสินค้า")
            return

        if not product_id or len(product_id) != 6 or product_id[0] == "0":
            self.view.show_message("ข้อผิดพลาด", "รหัสสินค้าต้องเป็นตัวเลข 6 หลัก และไม่ขึ้นต้นด้วย 0")
            return
        
        # ตรวจสอบรหัสสินค้าว่ามีในฐานข้อมูลหรือไม่
        if self.model.product_exists(product_id):
            self.view.show_message("ข้อผิดพลาด", "สินค้านี้มีอยู่ในระบบแล้ว")
            return
        
        # ตรวจสอบประเภทสินค้า
        if product_type == "อาหาร":
            # ถ้าประเภทสินค้าเป็นอาหาร ต้องกรอกวันที่หมดอายุ
            expiration_date = self.view.get_expiration_date()
            if not expiration_date:
                self.view.show_message("ข้อผิดพลาด", "กรุณากรอกวันที่หมดอายุ")
                return
            
            # ตรวจสอบว่า วันที่หมดอายุไม่เกินวันปัจจุบัน
            current_date = datetime.datetime.now().date()
            if expiration_date < current_date:
                self.view.show_message("ข้อผิดพลาด", "วันที่หมดอายุของสินค้าผ่านไปแล้ว ไม่สามารถเพิ่มสินค้าได้")
                # เพิ่มสินค้าลงใน rejected_products
                rejected_product = {"id": product_id, "type": product_type, "expiration_date": expiration_date, "rejected": True}
                self.model.add_product(rejected_product)  # เพิ่มสินค้าใน rejected_products
                self.rejected[product_type] += 1  # เพิ่มจำนวนสินค้าที่ปฏิเสธ
                self.update_labels()
                return

        elif product_type == "อิเล็กทรอนิกส์":
            # ถ้าประเภทสินค้าเป็นอิเล็กทรอนิกส์ ต้องไม่รับสินค้าที่เสียหายหรือไม่ตรวจสอบ
            condition = self.view.get_condition()
            if condition == "เสียหาย" or condition == "ต้องตรวจสอบเพิ่มเติม":
                self.view.show_message("ข้อผิดพลาด", "ไม่สามารถเพิ่มสินค้าที่เสียหายหรือจำเป็นต้องตรวจสอบเพิ่มเติม")
                # เพิ่มสินค้าลงใน rejected_products
                rejected_product = {"id": product_id, "type": product_type, "condition": condition, "rejected": True}
                self.model.add_product(rejected_product)  # เพิ่มสินค้าใน rejected_products
                self.rejected[product_type] += 1  # เพิ่มจำนวนสินค้าที่ปฏิเสธ
                self.update_labels()
                return
    
        elif product_type == "เสื้อผ้า":
            # ถ้าประเภทสินค้าเป็นเสื้อผ้า ต้องไม่รับสินค้าที่เสียหาย
            condition = self.view.get_condition()
            if condition == "เสียหาย":
                self.view.show_message("ข้อผิดพลาด", "ไม่สามารถเพิ่มสินค้าที่เสียหาย")
                # เพิ่มสินค้าลงใน rejected_products
                rejected_product = {"id": product_id, "type": product_type, "condition": condition, "rejected": True}
                self.model.add_product(rejected_product)  # เพิ่มสินค้าใน rejected_products
                self.rejected[product_type] += 1  # เพิ่มจำนวนสินค้าที่ปฏิเสธ
                self.update_labels()
                return

        # ถ้าประเภทสินค้าไม่มีปัญหา เพิ่มสินค้าใหม่
        product = {"id": product_id, "type": product_type}
        self.accepted[product_type] += 1
        self.update_labels()
        
        # ถ้าประเภทสินค้าเป็นอาหาร ต้องมีวันที่หมดอายุ
        if product_type == "อาหาร":
            product["expiration_date"] = expiration_date
        
        # ถ้าประเภทสินค้าเป็นอิเล็กทรอนิกส์หรือเสื้อผ้า ต้องมีสภาพสินค้า
        if product_type in ["อิเล็กทรอนิกส์", "เสื้อผ้า"]:
            product["condition"] = self.view.get_condition()
        
        self.model.add_product(product)
        self.view.show_message("สำเร็จ", "เพิ่มสินค้าเรียบร้อยแล้ว")

    def update_labels(self):
        # อัพเดทป้ายแสดงจำนวนสินค้าที่รับเข้าและปฏิเสธ
        self.view.accepted_text.config(text=f"อาหาร: {self.accepted['อาหาร']}\nอิเล็กทรอนิกส์: {self.accepted['อิเล็กทรอนิกส์']}\nเสื้อผ้า: {self.accepted['เสื้อผ้า']}")
        self.view.rejected_text.config(text=f"อาหาร: {self.rejected['อาหาร']}\nอิเล็กทรอนิกส์: {self.rejected['อิเล็กทรอนิกส์']}\nเสื้อผ้า: {self.rejected['เสื้อผ้า']}")
    
    def on_type_selected(self, event):
        self.view.on_type_selected()
