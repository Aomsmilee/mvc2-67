import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

class InventoryView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("ระบบนำเข้าข้อมูลคลังสินค้า")
        self.geometry("400x500")

        # ช่องกรอกรหัสสินค้า
        tk.Label(self, text="รหัสสินค้า (6 หลัก)").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        # ช่องเลือกประเภทสินค้า (OptionMenu หรือ Combobox)
        tk.Label(self, text="ประเภทสินค้า").pack()
        self.product_types = ["อาหาร", "อิเล็กทรอนิกส์", "เสื้อผ้า"]  # รายการประเภทสินค้า
        self.type_var = tk.StringVar(self)
        self.type_var.set(self.product_types[0])  # ค่าเริ่มต้น
        self.type_menu = ttk.Combobox(self, textvariable=self.type_var, values=self.product_types, state="readonly")
        self.type_menu.pack()

        # ช่องกรอกวันที่หมดอายุ (แสดงเมื่อเลือก "อาหาร")
        self.expiration_label = tk.Label(self, text="วันที่หมดอายุ (YYYY-MM-DD)")
        self.expiration_entry = tk.Entry(self)

        # ช่องเลือกสภาพสินค้า (แสดงตลอดเวลา)
        self.condition_label = tk.Label(self, text="สภาพสินค้า")
        self.condition_menu = ttk.Combobox(self, values=["ปกติ", "เสียหาย", "ต้องตรวจสอบเพิ่มเติม"], state="readonly")
        self.condition_menu.pack()

        # ปุ่มเพิ่มสินค้า
        self.add_product_button = tk.Button(self, text="เพิ่มสินค้า", command=self.controller.add_product)

        # แสดงจำนวนสินค้าที่รับเข้าและปฏิเสธที่ด้านล่าง
        self.accepted_label = tk.Label(self, text="จำนวนสินค้าที่รับเข้า:")
        self.accepted_text = tk.Label(self, text="อาหาร: 0\nอิเล็กทรอนิกส์: 0\nเสื้อผ้า: 0")

        self.rejected_label = tk.Label(self, text="จำนวนสินค้าที่ปฏิเสธ:")
        self.rejected_text = tk.Label(self, text="อาหาร: 0\nอิเล็กทรอนิกส์: 0\nเสื้อผ้า: 0")

        # ใช้ pack() โดยกำหนด side="bottom" เพื่อให้แสดงที่ด้านล่างสุด
        self.accepted_label.pack(side="bottom")
        self.accepted_text.pack(side="bottom")
        self.rejected_label.pack(side="bottom")
        self.rejected_text.pack(side="bottom")

    def get_product_info(self):
        # คืนค่ารหัสสินค้าและประเภทสินค้า
        return self.id_entry.get(), self.type_var.get()

    def get_expiration_date(self):
        # คืนค่าวันที่หมดอายุ ถ้ามีการกรอก
        expiration_date_str = self.expiration_entry.get()
        if expiration_date_str:
            try:
                expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
                return expiration_date
            except ValueError:
                self.show_message("ข้อผิดพลาด", "รูปแบบวันที่ไม่ถูกต้อง")
        return None

    def show_expiration_date_field(self, show):
        # แสดง/ซ่อนช่องกรอกวันที่หมดอายุ
        if show:
            self.expiration_label.pack()
            self.expiration_entry.pack()
        else:
            self.expiration_label.pack_forget()
            self.expiration_entry.pack_forget()

    def show_condition_date_field(self, show):
        # แสดง/ซ่อนช่องกรอกสภาพสินค้า
        if show:
            self.condition_label.pack()
            self.condition_menu.pack()
        else:
            self.condition_label.pack_forget()
            self.condition_menu.pack_forget()

    def show_add_product_button(self, show):
        # แสดง/ซ่อนปุ่มเพิ่มสินค้า
        if show:
            self.add_product_button.pack()
        else:
            self.add_product_button.pack_forget()

    def get_condition(self):
        # คืนค่าสภาพสินค้า
        condition = self.condition_menu.get()
        return condition if condition else None

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def on_type_selected(self):
        product_type = self.type_var.get()

        # ซ่อนปุ่มเพิ่มสินค้า เพื่อให้มันไปแสดงในตำแหน่งที่ถูกต้อง
        self.add_product_button.pack_forget()

        # ตรวจสอบประเภทสินค้าและแสดงช่องกรอกวันที่หมดอายุ
        if product_type == "อาหาร":
            self.show_expiration_date_field(True)
            self.show_condition_date_field(False)

        if product_type == "อิเล็กทรอนิกส์":
            self.show_expiration_date_field(False)
            self.show_condition_date_field(True)

        if product_type == "เสื้อผ้า":
            self.show_expiration_date_field(False)
            self.show_condition_date_field(True)

        # แสดงปุ่มเพิ่มสินค้าใหม่หลังช่องกรอกวันที่หมดอายุและสภาพสินค้า
        self.show_add_product_button(True)
