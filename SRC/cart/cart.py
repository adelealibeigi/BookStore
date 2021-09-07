from product.models import Book

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Book.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def add(self, product, quantity=1):
        product_id = str(product.id)
        # is there any product in cart from before?
        if product_id not in self.cart:
            # create a part named product_id in session cart
            self.cart[product_id] = {'quantity': 0, 'price': str(product.final_price),
                                     'org_price': str(product.price),'slug':str(product.slug)}
        # if exist
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def add_one(self, product):
        product_id = str(product.id)

        self.cart[product_id]['quantity'] += 1
        self.save()

    def remove_one(self, product):
        product_id = str(product.id)

        self.cart[product_id]['quantity'] -= 1
        self.save()
