from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = "inventory.json"

def load_inventory():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_inventory():
    with open(DATA_FILE, "w") as f:
        json.dump(inventory, f)

inventory = load_inventory()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", inventory=inventory)

@app.route("/add", methods=["POST"])  # <-- Make sure methods=["POST"] is here
def add_item():
    item = request.form.get("item").strip().lower()
    quantity = request.form.get("quantity")
    if item and quantity:
        quantity = int(quantity)
        today = datetime.now().strftime("%Y-%m-%d")
        if item in inventory:
            inventory[item]["quantity"] += quantity
            inventory[item]["date"] = today
        else:
            inventory[item] = {"quantity": quantity, "date": today}
        save_inventory()
    return redirect(url_for("home"))

@app.route("/update", methods=["POST"])  # <-- Make sure methods=["POST"] is here
def update_item():
    item = request.form.get("item").strip().lower()
    quantity = request.form.get("quantity")
    if item and quantity and item in inventory:
        inventory[item]["quantity"] = int(quantity)
        inventory[item]["date"] = datetime.now().strftime("%Y-%m-%d")
        save_inventory()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
