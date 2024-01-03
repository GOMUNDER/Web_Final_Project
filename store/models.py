from django.db import models
from django.contrib.auth.models import User


# class Customer include customer information after login
# OneToOne mean every letter capitalized, user can only have one customer and visa versa
# on_delete=models.CASCADE will delete customer if the user is deleted
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    #add image later

    def __str__(self):
        return self.name
     
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    #

    def __str__(self):
        return self.name
    
    # add property so website won't show error when one of the image is blank because it read from image url
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


# on_delete==models.SET_NULL mean if a customer is deleted, the order wouldn't be deleted just set to null
# so a customer can have many order
# if complete is false mean the cart is still open so u can add product but if complete=true, we need to add order to new cart
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=False)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    # calculate and get total for each item
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    # calculate and get total items in cart
    @property 
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
# in OrderItem, its many to one relationship, order is the cart, order item is item in the cart, cart can have may order item
# single order can have multiple order item
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # calculate and get total price for all item
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total

# in ShippingAddress, attach customer by set to models.SET_NULL for some reason if the order get deleted, customer still have the shipping address
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address