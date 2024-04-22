from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Load items from file
def load_items():
    try:
        with open("items.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

# Save items to file
def save_items(items):
    with open("items.txt", "w") as file:
        for item in items:
            file.write(item + "\n")

# Initialize items with data from file
items = load_items()

@app.route("/", methods=["GET", "POST"])
def index():
    global items
    if request.method == "POST":
        item = request.form["item"]
        items.append(item)
        save_items(items)
        return redirect("/")
    return render_template("index.html", enumerated_items=enumerate(items))

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    global items
    if request.method == "POST":
        new_item = request.form["item"]
        if 0 <= index < len(items):
            items[index] = new_item
            save_items(items)
        return redirect("/")
    return render_template("edit.html", index=index, item=items[index])

@app.route("/delete/<int:index>")
def delete(index):
    global items
    if 0 <= index < len(items):
        del items[index]
        save_items(items)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
