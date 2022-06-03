from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///inventory.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(3000))

    def __str__(self):
        return f"Inventory(id: {self.id}, name: {self.name}, price: {self.price}, image url: '{self.image_url}')"


# Pages

@app.route('/')
def home():
    inventory = Inventory.query.all()
    return render_template('index.html', inventory=inventory)


@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        url = request.form['url']
        inv = Inventory(name=name, price=price, image_url=url)
        db.session.add(inv)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_inventory.html')


@app.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = Inventory.query.filter_by(id=item_id).first()
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        url = request.form['url']
        item.name = name
        item.price = price
        item.url = url
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update_item.html', item=item)


@app.route('/delete_item/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    item = Inventory.query.filter_by(id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))


# Run

if __name__ == '__main__':
    app.run(debug=True)
