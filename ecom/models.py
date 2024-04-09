from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Category model
class Category(models.Model):
   sub_category=models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
   is_sub=models.BooleanField(default=False)
   name= models.CharField(max_length=200,null=True)
   slug = models.SlugField(max_length=200,unique=True)
   def __str__(self):
       return self.name



# Customer model
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
    
        
        
      
#Product model
class Product(models.Model):
    category =models.ManyToManyField (Category,related_name='product')
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    detail=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name

#Order model
class Orders(models.Model):
    STATUS =(
        ('Đang chờ xử lý','Đang chờ xử lý'),
        ('Xác nhận đặt hàng','Xác nhận đặt hàng'),
        ('Đang giao hàng','Đang giao hàng'),
        ('Đã giao hàng','Đã giao hàng'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    #quantity = models.CharField(null=True)

#Feedback model
class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name






#Post model
class Post(models.Model):
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)  # Thêm trường thời gian đăng
    post_image= models.ImageField(upload_to='post_image/',null=True,blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    


