from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',views.home,name="home"),
    path('customersignup', views.customer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='ecom/user/customerlogin.html'),name='customerlogin'),
    path('adminlogin', LoginView.as_view(template_name='ecom/admin/adminlogin.html'),name='adminlogin'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('my-order', views.my_order_view,name='my-order'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('contactus', views.contactus_view,name='contactus'),
    path('aboutus', views.aboutus_view),
    path('logout', LogoutView.as_view(template_name='ecom/core/logout.html'),name='logout'),
    path('customer-category', views.customer_category_view, name='customer-category'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('endow', views.endow_view),
    path('core-product', views.core_product_view, name='core-product'),
    path('aboutus_home', views.aboutus_home_view),
    path('feedback-home', views.feedback_home_view,name='feedback-home'),
    path('search', views.search_view,name='search'),
    path('detail_1_home', views.detail_1_home_view),
  # --------------------   ADMIN with customer URLS   ----------------------------
    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('update-customer/admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
       # --------------------   ADMIN with booking URLS  ------------------------------
    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),
    path('update-order/admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
     # --------------------   ADMIN with product URLS  ------------------------------
    path('admin-products', views.admin_products_view,name='admin-products'),
    path('admin-add-product', views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),
    path('update-product/admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
     # --------------------   ADMIN with post URLS  ------------------------------
    path('view-post', views.view_post_view,name='view-post'),
    path('delete-post/<int:pk>', views.delete_post_view,name='delete-post'),
    path('update-post/<int:pk>', views. update_post_view,name='update-post'),
    path('admin-add-post', views.admin_add_post_view,name='admin-add-post'),
    
      # ------------------   ADMIN FeedBack ------------------------------------
    path('view-feedback', views.view_feedback_view,name='view-feedback'),
    
     
    path('order/', views.get_order_from_api, name='get_order_from_api'),
    path('create-order/',views.create_order_to_api, name='create_order'),
    path('map/',views.view_map, name='map'),
    
    
      #------------------------     ADMIN URLS     ------------------------------
    #--------------------------------------------------------------------------
    path('adminlogin', LoginView.as_view(template_name='ecom/admin/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('adminclick', views.adminclick_view),
    
     # ------------------    URLS    --------------------------------------
    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'), 
    path('payment-success', views.payment_success_view,name='payment-success'),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),
    
    
    path('category', views.category, name='category'),
    
    path('detail', views.detail, name='detail'),
    path('post_detail', views.blog, name='post_detail'),
    path('SignupSuccess', LogoutView.as_view(template_name='ecom/core/SignupSuccess.html'),name='SignupSuccess'),
   
]


