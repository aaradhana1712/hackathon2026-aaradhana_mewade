import json
import os

class DataManager:
    def __init__(self, data_dir="sample_data"):
        self.data_dir = data_dir
        self.customers = self._load_json("customers.json")
        self.orders = self._load_json("orders.json")
        self.products = self._load_json("products.json")
        self.tickets = self._load_json("tickets.json")
        with open(os.path.join(data_dir, "knowledge-base.md"), "r", encoding="utf-8") as f:
            self.knowledge_base = f.read()

    def _load_json(self, filename):
        path = os.path.join(self.data_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_customer(self, email):
        for c in self.customers:
            if c["email"] == email:
                return c
        return None

    def get_order(self, order_id):
        for o in self.orders:
            if o["order_id"] == order_id:
                return o
        return None

    def get_product(self, product_id):
        for p in self.products:
            if p["product_id"] == product_id:
                return p
        return None
