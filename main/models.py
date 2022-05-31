from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

CATEGORY_CHOICES = (
    ("P", "Pack"),
    ("B", "Beat")
    
)
LABEL_CHOICES = (
    ("P", "primary"),
    ("S", "secondary"),
    ("D", "danger")
)


# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=2,default="S")
    # label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(default="",blank = True, null=False, db_index=True)
    
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)        

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart",kwargs={
            "slug":self.slug
        })        

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart",kwargs={
            "slug":self.slug
        })        

    # class Meta:
    #     abstract= True
    #     ordering = ["title"]

class Beat(Item):
    bpm = models.FloatField()
    key = models.CharField(max_length=5)
    category = models.CharField(default="Beat",max_length=10)
    genre = models.CharField(null=True, max_length=15)
    bpm = models.IntegerField(
        validators= [MinValueValidator(50),MaxValueValidator(200)])
    file = models.FileField(upload_to="static/beats")
    image = models.ImageField(upload_to="static/beats/img")
    is_newest = models.BooleanField(default=False)



    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.Name)
    #     super().save(*args, **kwargs)

class Pack(Item):
    sample_count = models.FloatField()
    category = models.CharField(default="Pack",max_length=10)
    image = models.ImageField(upload_to="static/packs/img")   
    file = models.FileField(upload_to="static/packs")

    is_newest = models.BooleanField(default=False)
  


    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.Name)
    #     super().save(*args, **kwargs)
            

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity*self.item.price

    def get_total_discount_price(self):
        return self.quantity*self.item.discount_price
        
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey("BillingAddress", on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey("Payment",on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total



class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    charge_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username