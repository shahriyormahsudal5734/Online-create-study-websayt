from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class Viloyat1(models.Model):
    title = models.CharField(max_length=40)
    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=40)
    def __str__(self):
        return self.title

class Oquv_Markaz1(models.Model):
    title = models.CharField(max_length=40)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='markazimg/')
    rating = models.CharField(max_length=50,blank=True)
    number = models.CharField(max_length=12)
    checking = models.BooleanField()
    applys = models.CharField(max_length=50,blank=True)
    telegram = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    youtobe = models.URLField(blank=True)
    viloyat1 = models.ForeignKey(Viloyat1,on_delete=models.CASCADE)
    manzil = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('room', kwargs={'id': self.id})
    
    
class Kurs(models.Model):
    markaz = models.ForeignKey(Oquv_Markaz1,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    viloyatlar = models.ForeignKey(Viloyat1,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='kurs/')
    davomiyligi = models.CharField(max_length=50)
    price = models.IntegerField()
    applys = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.title


class Ariza(models.Model):
    category =models.ForeignKey(Kurs,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='ariza/')
    age = models.IntegerField()
    number = models.CharField(max_length=12)
    ariza_chek = models.BooleanField(blank=True)


    def __str__(self):
        return self.title