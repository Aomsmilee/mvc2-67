from inventory_controller import InventoryController

if __name__ == "__main__":
    app = InventoryController()
    app.view.mainloop()  # ใช้ mainloop() ของ view แทน
