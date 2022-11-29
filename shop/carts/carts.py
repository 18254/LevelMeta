from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import db , app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories
import json
#importing db file to be used in the carts function 

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
#allows multiple products to be added to the shopping cart 

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        # quantity from how many user wants to add to cart default "min" equal to 1 
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()
        #adds user selected variables to the cart 

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors}}
            #information eg. name, price etc. comes from the dtatabase
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    #stores item in a new database called carts 
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
                    #allows for more than one product to be added to the shopping cart
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
        #error message catches everything with exception statement 
    finally:
        return redirect(request.referrer)
   



@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    #starting price eg no products in cart
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        #discount aplyed to product
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax =("%.2f" %(.15 * float(subtotal)))
        #gst added to purchase 
        grandtotal = float("%.2f" % (1.15 * subtotal))
        #grandtoal gst + sale price 
    return render_template('products/carts.html',tax=tax, grandtotal=grandtotal,brands=brands(),categories=categories())
    #shopping cart page displays user products



@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        #user updating the amount or color being diffrent editions of the game 
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!')
                    return redirect(url_for('getCart'))
                    #updating tax and grand total visual promt for user that it has happened 
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))



@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
        #if all items are deleted redirects user back to the home page 
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
                #deletes singlar items from the shopping cart 
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
        #rids of all items from the cart returns user back to home 
    except Exception as e:
        print(e)
