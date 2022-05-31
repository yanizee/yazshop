from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from .forms import CheckoutForm
from  django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView,View
from .models import *
import datetime
# Create your views here.

# 
def about(request):
    return render(request,"main/about.html")

def licences(request):
    return render(request,"main/licences.html")



def login(request):
    return render(request,"main/account/login.html")

def item_list(request):
    context = {
        "items" : Item.objects.all()
    }
    return render(request,"main/item_list.html",context)


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = "main/index.html"

# def index(request):
#     context = {
#         "items" : Item.objects.all()
#     }
#     return render(request,"main/home-page.html", context)

class ItemDetailView(DetailView):
    model = Item
    template_name= "main/product-page.html"

    def get_object(self, queryset=None):
        return Item.objects.get(slug=self.kwargs.get("slug"))
    # def get(self,*arg,**kwargs):
    #     context = {
    #         "items" : Item.objects.all(slug=self.slug)
    #     }
    #     return render(self.request,"main/product-page.html",context)

def Product_Page(request,slug):
    context = {
    "items" : Item.objects.get(slug=slug)
    }
    return render(request,"main/product-page.html",context)
    
    

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user,ordered=False) #only get order that not has been completed
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists(): 
            
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"Quantity was updated.")
        else:
            messages.info(request,"This Item was added to your cart!")
            order.items.add(order_item)             
    else: 
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This Item was added to your cart!")
    return redirect("order-summary")


@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False) #only get order that not has been completed
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists(): 
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This Item was removed from your cart!")
            return redirect("order-summary")  
        else:
            #message saying order does not contain that item
            messages.info(request,"This Item was not in your cart!")
            return redirect("product",slug=slug)  
    else:
        #add a message saying the user doesnt have an order
        messages.info(request,"You do not have an active order")
        return redirect("order-summary")

@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False) #only get order that not has been completed
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists(): 
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else: order.items.remove(order_item)
            messages.info(request,"Quantity was updated")
            return redirect("order-summary")  
        else:
            #message saying order does not contain that item
            messages.info(request,"This Item was not in your cart!")
            return redirect("product",slug=slug)  
    else:
        #add a message saying the user doesnt have an order
        messages.info(request,"You do not have an active order")
        return redirect("product",slug=slug)            
      


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*arg,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "objects":order
            }
            return render(self.request,"main/order-summary.html",context)

        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("/")


class CheckoutView(View):
    def get(self,*args,**kwargs):
        #form
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                "form":form,
                "objects":order,
            }
            return render(self.request,"main/checkout-page.html",context)   
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("/")
    
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                street_address = form.cleaned_data.get(street_address) 
                apartment_address = form.cleaned_data.get(apartment_address)
                country = form.cleaned_data.get(country)
                zip = form.cleaned_data.get(zip)
                #todo
                # same_shipping_address = form.cleaned_data.get(same_shipping_address)
                # save_info = form.cleaned_data.get(save_info)
                payment_option = form.cleaned_data.get(payment_option)

                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
            	#redirect to selected payment method
                return redirect("checkout")
            messages.warning(self.request,"Failed checkout")
            return redirect("checkout")

        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("order-summary")

def payment_complete(request):
    if request.method == "POST":
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user,ordered=False,id=body["orderID"])
        payment = Payment(
            user=request.user,
            charge_id = body["Data"],
            amount = order.get_total()
        )
        payment.save()

        # assign the payment to order
        order.payment = payment
        order.ordered = True
        order.save()
        # messages.success(request,"payment was successfull")
        # print(body)
        return redirect("order-complete-page")

def order_complete_page(request,pk):
    order_qs = Order.objects.get(user=request.user,ordered=True,pk=pk)
    orderitems = OrderItem.objects.filter(order=order_qs)
    current_datetime = datetime.datetime.now().date()
    context = {
        "objects":orderitems,
        "order":order_qs,
        "date":current_datetime,
    }
    return render(request,"main/payment_complete.html",context)





 


