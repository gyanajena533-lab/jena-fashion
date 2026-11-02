import os, secrets
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product, Order, OrderItem, Review

app = Flask(__name__)
app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev-only-change-this-secret', SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL','sqlite:///jena_fashion.db').replace('postgres://','postgresql://'), SQLALCHEMY_TRACK_MODIFICATIONS=False, MAX_CONTENT_LENGTH=5*1024*1024)
db.init_app(app)
login_manager=LoginManager(app); login_manager.login_view='login'; login_manager.login_message='Please log in to continue.'
@login_manager.user_loader
def load_user(uid): return db.session.get(User,int(uid))

SEED=[('Royal Pink Silk Saree','saree','Elegant silk-look saree for celebrations.',1499,2199,'BESTSELLER','https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=85'),('Classic Heritage Saree','saree','A timeless drape for special occasions.',1799,2499,'POPULAR','https://images.unsplash.com/photo-1583391733958-d7a05b7f0b5b?auto=format&fit=crop&w=700&q=85'),('Everyday Grace Kurta','kurta','Comfortable style for everyday wear.',899,1299,'VALUE PICK','https://images.unsplash.com/photo-1583391733981-849c9e4c7b7a?auto=format&fit=crop&w=700&q=85'),('Elegant Blossom Suit','kurta','A graceful suit set for your wardrobe.',1199,1699,'TRENDING','https://images.unsplash.com/photo-1597983073493-88cd35cf93b0?auto=format&fit=crop&w=700&q=85'),('Festive Celebration Dress','dress','A festive outfit for memorable moments.',1999,2799,'FESTIVE','https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=700&q=85'),('Golden Occasion Wear','dress','Statement occasion wear.',2299,3199,'NEW ARRIVAL','https://images.unsplash.com/photo-1610030469668-8e9f641aafc4?auto=format&fit=crop&w=700&q=85')]
with app.app_context():
 db.create_all()
 if Product.query.count()==0:
  for n,c,d,p,o,t,i in SEED: db.session.add(Product(name=n,category=c,description=d,price=p,old_price=o,tag=t,image=i,stock=10))
  db.session.commit()
 # Create first admin only when explicit environment variables are configured.
 email=os.environ.get('JENA_ADMIN_EMAIL'); password=os.environ.get('JENA_ADMIN_PASSWORD')
 if email and password and not User.query.filter_by(email=email.lower()).first():
  db.session.add(User(name='Jena Admin',email=email.lower(),password_hash=generate_password_hash(password),is_admin=True)); db.session.commit()

def admin_required(fn):
 @wraps(fn)
 @login_required
 def wrapped(*a,**kw):
  if not current_user.is_admin: abort(403)
  return fn(*a,**kw)
 return wrapped

def cart_data():
 cart=session.get('cart',{}); items=[]; total=0
 for key,qty in cart.items():
  p=db.session.get(Product,int(key))
  if p and qty>0:
   sub=p.price*qty; total+=sub; items.append({'product':p,'quantity':qty,'subtotal':sub})
 return items,total
@app.context_processor
def common():
 return {'cart_count':sum(session.get('cart',{}).values()),'categories':['saree','kurta','dress']}
@app.route('/')
def home():
 products=Product.query.order_by(Product.created_at.desc()).all(); return render_template('index.html',products=products)
@app.route('/products')
def products():
 q=request.args.get('q','').strip(); category=request.args.get('category',''); query=Product.query
 if q: query=query.filter(Product.name.ilike(f'%{q}%')|Product.description.ilike(f'%{q}%'))
 if category in ('saree','kurta','dress'): query=query.filter_by(category=category)
 return render_template('products.html',products=query.order_by(Product.created_at.desc()).all(),q=q,category=category)
@app.route('/product/<int:pid>')
def product_detail(pid):
 p=Product.query.get_or_404(pid); reviews=Review.query.filter_by(product_id=pid).order_by(Review.created_at.desc()).all(); avg=db.session.query(db.func.avg(Review.rating)).filter_by(product_id=pid).scalar()
 return render_template('product_detail.html',product=p,reviews=reviews,average=round(avg or 0,1))
@app.route('/cart/add/<int:pid>',methods=['POST'])
def add_to_cart(pid):
 p=Product.query.get_or_404(pid); cart=session.get('cart',{}); k=str(pid); qty=int(cart.get(k,0))
 if p.stock<1: flash('This item is out of stock.','error')
 elif qty>=p.stock or qty>=10: flash('Maximum available quantity reached.','error')
 else: cart[k]=qty+1; session['cart']=cart; flash('Added to your cart.','success')
 return redirect(request.referrer or url_for('view_cart'))
@app.route('/cart')
def view_cart():
 items,total=cart_data(); return render_template('cart.html',cart_items=items,total_price=total,total_quantity=sum(x['quantity'] for x in items))
@app.route('/cart/update/<int:pid>',methods=['POST'])
def update_cart(pid):
 p=Product.query.get_or_404(pid); qty=request.form.get('quantity',type=int); cart=session.get('cart',{})
 if qty is not None and 1<=qty<=min(10,p.stock): cart[str(pid)]=qty
 else: flash('Enter a valid quantity available in stock.','error')
 session['cart']=cart; return redirect(url_for('view_cart'))
@app.route('/cart/remove/<int:pid>',methods=['POST'])
def remove_from_cart(pid):
 cart=session.get('cart',{}); cart.pop(str(pid),None); session['cart']=cart; return redirect(url_for('view_cart'))
@app.route('/register',methods=['GET','POST'])
def register():
 if request.method=='POST':
  name=request.form.get('name','').strip(); email=request.form.get('email','').strip().lower(); password=request.form.get('password','')
  if not name or len(password)<8: flash('Enter your name and a password of at least 8 characters.','error')
  elif User.query.filter_by(email=email).first(): flash('An account with that email already exists.','error')
  else:
   u=User(name=name,email=email,password_hash=generate_password_hash(password)); db.session.add(u); db.session.commit(); login_user(u); return redirect(url_for('home'))
 return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  u=User.query.filter_by(email=request.form.get('email','').strip().lower()).first()
  if u and check_password_hash(u.password_hash,request.form.get('password','')): login_user(u); return redirect(request.args.get('next') or url_for('home'))
  flash('Email or password is incorrect.','error')
 return render_template('login.html')
@app.route('/logout')
@login_required
def logout(): logout_user(); return redirect(url_for('home'))
@app.route('/review/<int:pid>',methods=['POST'])
@login_required
def add_review(pid):
 Product.query.get_or_404(pid); rating=request.form.get('rating',type=int); comment=request.form.get('comment','').strip()
 if rating not in range(1,6): flash('Choose a rating from 1 to 5.','error')
 else:
  old=Review.query.filter_by(product_id=pid,user_id=current_user.id).first()
  if old: old.rating=rating; old.comment=comment
  else: db.session.add(Review(user_id=current_user.id,product_id=pid,rating=rating,comment=comment))
  db.session.commit(); flash('Thank you for your review.','success')
 return redirect(url_for('product_detail',pid=pid))
@app.route('/checkout',methods=['GET','POST'])
@login_required
def checkout():
 items,total=cart_data()
 if not items: flash('Your cart is empty.','error'); return redirect(url_for('view_cart'))
 if request.method=='POST':
  name=request.form.get('name','').strip(); phone=request.form.get('phone','').strip(); address=request.form.get('address','').strip(); payment=request.form.get('payment','cod')
  if not name or not phone or not address: flash('Please complete all delivery details.','error')
  elif payment!='cod': flash('Online payment is not activated yet. Choose Cash on Delivery for this test order.','error')
  elif any(x['quantity']>x['product'].stock for x in items): flash('Some product stock changed. Please review your cart.','error')
  else:
   order=Order(user_id=current_user.id,customer_name=name,email=current_user.email,phone=phone,address=address,total_amount=total,payment_status='Unpaid')
   db.session.add(order); db.session.flush()
   for x in items:
    p=x['product']; db.session.add(OrderItem(order_id=order.id,product_id=p.id,quantity=x['quantity'],price=p.price)); p.stock-=x['quantity']
   db.session.commit(); session['cart']={}; return redirect(url_for('order_success',oid=order.id))
 return render_template('checkout.html',cart_items=items,total_price=total)
@app.route('/order/<int:oid>')
@login_required
def order_success(oid):
 order=Order.query.filter_by(id=oid,user_id=current_user.id).first_or_404(); return render_template('order_success.html',order=order)
@app.route('/account/orders')
@login_required
def my_orders(): return render_template('orders.html',orders=Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all())
@app.route('/admin')
@admin_required
def admin(): return render_template('admin.html',products=Product.query.order_by(Product.id.desc()).all(),orders=Order.query.order_by(Order.created_at.desc()).all())
@app.route('/admin/product/new',methods=['GET','POST'])
@app.route('/admin/product/<int:pid>/edit',methods=['GET','POST'])
@admin_required
def edit_product(pid=None):
 p=Product.query.get_or_404(pid) if pid else Product()
 if request.method=='POST':
  try:
   p.name=request.form['name'].strip(); p.category=request.form['category']; p.description=request.form.get('description','').strip(); p.price=int(request.form['price']); p.old_price=int(request.form.get('old_price') or 0) or None; p.image=request.form.get('image','').strip(); p.tag=request.form.get('tag','').strip(); p.stock=int(request.form['stock'])
   if not p.name or p.price<1 or p.stock<0 or p.category not in ('saree','kurta','dress'): raise ValueError()
   db.session.add(p); db.session.commit(); flash('Product saved.','success'); return redirect(url_for('admin'))
  except (ValueError,KeyError): flash('Check the product details and try again.','error')
 return render_template('product_form.html',product=p)
@app.route('/admin/product/<int:pid>/delete',methods=['POST'])
@admin_required
def delete_product(pid):
 p=Product.query.get_or_404(pid)
 if OrderItem.query.filter_by(product_id=pid).first(): p.stock=0; flash('Product has order history, so it was set out of stock instead of deleted.','success')
 else: db.session.delete(p); flash('Product deleted.','success')
 db.session.commit(); return redirect(url_for('admin'))
@app.route('/admin/order/<int:oid>',methods=['POST'])
@admin_required
def update_order(oid):
 o=Order.query.get_or_404(oid); status=request.form.get('status')
 if status in ('Pending','Processing','Shipped','Delivered','Cancelled'): o.status=status; db.session.commit()
 return redirect(url_for('admin'))
@app.errorhandler(403)
def forbidden(e): return render_template('message.html',title='Access denied',message='This page is only for the store administrator.'),403
if __name__=='__main__': app.run(debug=os.environ.get('FLASK_DEBUG')=='1')
