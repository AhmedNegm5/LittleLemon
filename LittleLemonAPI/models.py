from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True,blank=True,null=True)
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)
        
        
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True,blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(MenuItem,self).save(*args,**kwargs)
        
        

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'
    
    def get_total_price(self):
        return self.item.price * self.quantity
    

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}\'s order'
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total
    

