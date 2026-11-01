from flask import Flask, render_template
app = Flask(__name__)

PRODUCTS = [
 {"id":1,"name":"Royal Pink Silk Saree","category":"saree","price":1499,"old":2199,"tag":"BESTSELLER","image":"https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=85"},
 {"id":2,"name":"Classic Heritage Saree","category":"saree","price":1799,"old":2499,"tag":"POPULAR","image":"https://images.unsplash.com/photo-1583391733958-d7a05b7f0b5b?auto=format&fit=crop&w=700&q=85"},
 {"id":3,"name":"Everyday Grace Kurta","category":"kurta","price":899,"old":1299,"tag":"VALUE PICK","image":"https://images.unsplash.com/photo-1583391733981-849c9e4c7b7a?auto=format&fit=crop&w=700&q=85"},
 {"id":4,"name":"Elegant Blossom Suit","category":"kurta","price":1199,"old":1699,"tag":"TRENDING","image":"https://images.unsplash.com/photo-1597983073493-88cd35cf93b0?auto=format&fit=crop&w=700&q=85"},
 {"id":5,"name":"Festive Celebration Dress","category":"dress","price":1999,"old":2799,"tag":"FESTIVE","image":"https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=700&q=85"},
 {"id":6,"name":"Golden Occasion Wear","category":"dress","price":2299,"old":3199,"tag":"NEW ARRIVAL","image":"https://images.unsplash.com/photo-1610030469668-8e9f641aafc4?auto=format&fit=crop&w=700&q=85"}
]
@app.route("/")
def home():
 return render_template("index.html", products=PRODUCTS)
if __name__ == "__main__":
 app.run(debug=True)
