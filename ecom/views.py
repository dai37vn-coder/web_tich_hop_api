from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import requests
import json







def get_order_from_api(request):
    order_code = request.GET.get('order_code')  # query parameter

    if order_code:  # Kiểm tra 
        api_url = 'https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/detail'
        api_key = '1274b149-94ab-11ee-a6e6-e60958111f48'  

        headers = {
            'Content-Type': 'application/json',
            'Token': api_key,
        }

        params = {
            "order_code": order_code,
        }

        api_data = None
        error_message = None

        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()  # Kiểm tra lỗi HTTP

            api_response = response.json()
            api_data = api_response.get('data')
            if not api_data:
                error_message = "Không có dữ liệu trả về từ API"
        except requests.exceptions.HTTPError as http_err:
            error_message = f'Lỗi HTTP: {http_err}'
        except Exception as e:
            error_message = f'Lỗi: {e}'

        if error_message:
            return render(request, 'ecom/admin/error.html', {'error_message': error_message})
        else:
            return render(request, 'ecom/admin/order_detail.html', {'data': api_data})
    else:
        error_message = "Mã vận đơn không được cung cấp."
        return render(request, 'ecom/admin/error.html', {'error_message': error_message})


# Create your views here.
def home(request) :
    return render(request,'ecom/home.html')



def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'ecom/user/customersignup.html',context=mydict)


#checking user is customer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()



#CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')
    
    
    #---------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    products=models.Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    posts = Post.objects.all() 
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
       
    return render(request,'ecom/user/customer_home.html',{'products':products,'posts':posts,'categories':categories,'product_count_in_cart':product_count_in_cart})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'ecom/user/my_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'ecom/user/edit_profile.html',context=mydict)


    
    #for showing login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    orders=models.Orders.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request,'ecom/user/my_order.html',{'data':zip(ordered_products,orders)})



def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/core/feedback_sent.html')
    return render(request, 'ecom/core/send_feedback.html', {'feedbackForm':feedbackForm})

def feedback_home_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/core/feedback_sent.html')
    return render(request, 'ecom/core/feedback_home.html', {'feedbackForm':feedbackForm})




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def core_product_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/core/product.html',{'products':products,'product_count_in_cart':product_count_in_cart})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_category_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/user/customer_category.html',{'products':products,'product_count_in_cart':product_count_in_cart})










# here we are just directing to this view...actually we have to check whther payment is successful or not
#then only this view should be accessed
@login_required(login_url='customerlogin')
def payment_success_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    products=None
    email=None
    mobile=None
    address=None
    
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            # Here we get products list that will be ordered by one customer at a time

    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']
        

    # here we are placing number of orders as much there is a products
    # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
    for product in products:
        models.Orders.objects.get_or_create(customer=customer,product=product,status='Đang chờ xử lý',email=email,mobile=mobile,address=address)

    # after order placed cookies should be deleted
    response = render(request,'ecom/user/payment_success.html')
    response.delete_cookie('product_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
   
    return response





# shipment address before placing order
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            
            email = addressForm.cleaned_data['Email']
            mobile=addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
      
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
            total=0
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in = product_id_in_cart)
                    for p in products:
                        total=total+p.price

            response = render(request, 'ecom/user/payment.html',{'total':total})
            response.set_cookie('email',email)
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
           
            return response
    return render(request,'ecom/user/customer_address.html',{'addressForm':addressForm,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})


#for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return





@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,productID):
    order=models.Orders.objects.get(id=orderID)
    product=models.Product.objects.get(id=productID)
    mydict={
        'orderDate':order.order_date,
        'customerName':request.user,
        'customerEmail':order.email,
        'customerMobile':order.mobile,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.product_image,
        'productPrice':product.price,
        'productDescription':product.description,


    }
    return render_to_pdf('ecom/user/download_invoice.html',mydict)
 





#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='adminlogin')
def create_order_to_api(request):
    if request.method == 'POST':
        return redirect('success_page')
    return render(request,'ecom/admin/create_order.html')
def success_page(request):
    return render(request,'ecom/admin/success.html')


@login_required(login_url='adminlogin')
def view_map(request):
    return render(request,'ecom/admin/map.html')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'ecom/admin/admin-view/admin_dashboard.html',context=mydict)

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'ecom/admin/admin-booking/update_order.html',{'orderForm':orderForm})

# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'ecom/admin/admin-cus/view_customer.html',{'customers':customers})


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'ecom/admin/admin-cus/admin_update_customer.html',context=mydict)
# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'ecom/admin/admin-booking/admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})

@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# admin view the product
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'ecom/admin/admin-prod/admin_products.html',{'products':products})




# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'ecom/admin/admin-prod/admin_add_products.html',{'productForm':productForm})

@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'ecom/admin/admin-prod/admin_update_product.html',{'productForm':productForm})

# admin view the feedback
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'ecom/admin/view_feedback.html',{'feedbacks':feedbacks})




#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'ecom/core/aboutus.html')

def aboutus_home_view(request):
    return render(request,'ecom/core/aboutus_home.html')

def detail_1_home_view(request):
    return render(request,'ecom/core/detail_1_home.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'ecom/core/contactussuccess.html')
    return render(request, 'ecom/core/contactus.html', {'form':sub})

def endow_view(request):
    return render(request,'ecom/core/endow.html')





#   ---------------------------------------------------------------------------------
#   ------------------------ PUBLIC CUSTOMER RELATED VIEWS START --------------------
#   ---------------------------------------------------------------------------------

def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Kết quả tìm kiếm :"

    if request.user.is_authenticated:
        return render(request,'ecom/user/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'ecom/core/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})



# any one can add product to cart, no need of signin
def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'ecom/core/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product=models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' đã thêm vào giỏ hàng thành công!')

    return response



# for checkout of cart
def cart_view(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for p in products:
                total=total+p.price
    return render(request,'ecom/core/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'ecom/core/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response
    
    
    
    #Detail product
def detail(request):
    pass






#category
from .models import Category,Product
from django.shortcuts import render

def category(request):

    categories = Category.objects.filter(is_sub=False)
    active_category=request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context={'categories':categories,'products':products,'active_category':active_category}
    return render(request, 'ecom/core/category.html',context)




#detail 
def detail(request):
    if request.user.is_authenticated:
        customer =request.user       
        user_not_login="hidden"
        user_login="Show"
    else:
       items=[]     
       user_not_login="show"
       user_login="hidden"
    id=request.GET.get('id','')
    products=Product.objects.filter(id=id)
    
    categories=Category.objects.filter(is_sub=False)
    context={'categories':categories,'products':products,'user_not_login':user_not_login,' user_login': user_login}
    return render(request, 'ecom/core/detail.html',context)
        






#post
from .models import Post
def blog(request):
    id=request.GET.get('id','')
    posts = Post.objects.filter(id=id)  # Lấy tất cả các bài viết từ CSDL
    return render(request, 'ecom/core/post_detail.html', {'posts': posts})





# admin view post
@login_required(login_url='adminlogin')
def view_post_view(request):
    posts=models.Post.objects.all()
    return render(request,'ecom/admin/admin-post/admin_view_post.html',{'posts':posts})

# admin delete post
@login_required(login_url='adminlogin')
def delete_post_view(request, pk):
    # Lấy đối tượng post dựa trên khóa chính (pk) được cung cấp hoặc trả về 404 nếu không tìm thấy
    post = get_object_or_404(models.Post, id=pk)

    # Kiểm tra xem người dùng có quyền xóa bài viết không (nếu cần)
    # Ví dụ: if not request.user.has_perm('delete_post', post):
    #         return HttpResponseForbidden("Bạn không có quyền xóa bài viết này.")

    # Lưu tên tác giả trước khi xóa bài viết
    author_name = post.author.username

    # Xóa bài viết
    post.delete()

    messages.success(request, f'Bài viết của người đăng {author_name} đã được xóa thành công.')

    return redirect('view-post')





# admin update post
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import models, forms
from django.contrib.auth.decorators import login_required
@login_required(login_url='adminlogin')
def update_post_view(request, pk):
    # Lấy đối tượng post dựa trên khóa chính (pk) được cung cấp hoặc trả về 404 nếu không tìm thấy
    post = get_object_or_404(models.Post, id=pk)

    # Kiểm tra xem người dùng có quyền cập nhật bài viết không (nếu cần)
    # Ví dụ: if not request.user.has_perm('change_post', post):
    #         return HttpResponseForbidden("Bạn không có quyền cập nhật bài viết này.")

    # Nếu form được gửi qua phương thức POST
    if request.method == 'POST':
        postForm = forms.PostForm(request.POST, request.FILES, instance=post)

        # Kiểm tra xem form có hợp lệ không
        if postForm.is_valid():
            postForm.save()  # Lưu thông tin post đã được cập nhật
            messages.success(request, 'Bài viết đã được cập nhật thành công.')
            return redirect('view-post')  # Chuyển hướng đến URL 'view-posts' (điều chỉnh nếu cần)
        else:
            messages.error(request, 'Có lỗi xảy ra trong quá trình cập nhật bài viết.')

    else:
        # Nếu không phải là yêu cầu POST, tạo một thể hiện của PostForm, được điền trước với dữ liệu hiện tại
        postForm = forms.PostForm(instance=post)

    # Hiển thị template với form
    return render(request, 'ecom/admin/admin-post/admin_update_post.html', {'postForm': postForm, 'post': post})


# admin add post
from datetime import datetime
@login_required(login_url='adminlogin')
def admin_add_post_view(request):
    if request.method == 'POST':
        postForm = forms.PostForm(request.POST, request.FILES)
        if postForm.is_valid():
            # Format thời gian ở đây, ví dụ "%d/%m/%Y %H:%M:%S"
            postForm.instance.published_at = datetime.strptime(request.POST['published_at'], '%d/%m/%Y %H:%M:%S')
            postForm.save()
            return redirect('view-post')
    else:
        postForm = forms.PostForm()

    return render(request, 'ecom/admin/admin-post/admin_add_post.html', {'postForm': postForm})