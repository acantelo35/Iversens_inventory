from flask import Flask, request, render_template, redirect
from datetime import datetime

app = Flask(__name__)
inventory = {}
last_updated = None

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", inventory=inventory, last_updated=last_updated)

@app.route("/add", methods=["POST"])
def add_item():
    item = request.form.get("item")
    quantity = request.form.get("quantity")
    if item and quantity:
        inventory[item] = inventory.get(item, 0) + int(quantity)
        update_timestamp()
    return redirect("/")

@app.route("/update", methods=["POST"])
def update_item():
    item = request.form.get("item")
    quantity = request.form.get("quantity")
    if item and quantity:
        inventory[item] = int(quantity)
        update_timestamp()
    return redirect("/")

def update_timestamp():
    global last_updated
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    app.run(debug=True)
