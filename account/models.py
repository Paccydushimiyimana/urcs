from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name=models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Sub_category(models.Model):
    category = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class College(models.Model):
    name=models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    
class School(models.Model):
    name=models.CharField(max_length=30, unique=True)
    college=models.ForeignKey(College, related_name='schools', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.CharField(max_length=30, unique=True)
    levels=models.PositiveIntegerField(default=4)
    school=models.ForeignKey(School, related_name='departments',on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class MyUser(AbstractUser):
    image = models.ImageField(upload_to='profiles/',default='avatar.png')
    phone = models.CharField(max_length=10, null=True)
    college=models.ForeignKey(College, related_name='users', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, related_name='users', on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(Sub_category, related_name='users', on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, related_name='users', on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, related_name='users', on_delete=models.CASCADE, null=True)
    level = models.CharField(max_length=5, null=True)
    unreads = models.PositiveIntegerField(default=0)
    
