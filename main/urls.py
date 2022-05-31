from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('about/', about, name="about"),
    path('licences/', licences, name="licences"),
    path("product/<slug>/",ItemDetailView.as_view(),name="product"),
    # path("product/<slug>/",Product_Page,name="product"),
    path("add-to-cart/<slug>/",add_to_cart,name="add-to-cart"),
    path("remove-from-cart/<slug>/",remove_from_cart,name="remove-from-cart"),
    path("remove-item-from-cart/<slug>/",remove_single_item_from_cart,name="remove-single-item-from-cart"),
    
    path("checkout/",CheckoutView.as_view(),name="checkout"),
    path("order-summary/",OrderSummaryView.as_view(),name="order-summary"),

    path("login/",login,name="login"),
    
    path("payment_complete/",payment_complete,name="payment-completed"),
    path("thank_you/<pk>/",order_complete_page,name="order-complete-page"),
    # path("thank_you/",orderCompletePage.as_view(),name="order-complete-page"),

    # path("payment/",paymentView.as_view(),name="payment"), #ghosturl
    # path("payment/<payment_option>",PaymentView.as_view(),name="payment")
]

# from js_urls.views import JsUrlsView

# urlpatterns = [
#     # other urls
#     path(r'^js-urls/$', JsUrlsView.as_view(), name='js_urls'),
# ]