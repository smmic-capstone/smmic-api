from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
import uuid
class AppUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, province, city, barangay, zone, zip_code, email, password=None):
            if not email:
                raise ValueError('An Email is Required')
            if not password:
                raise ValueError('A Password is Required')
            
            email = self.normalize_email(email)
            user = self.model(
                 first_name=first_name, 
                 last_name=last_name,
                 province=province, 
                 city=city, 
                 barangay=barangay, 
                 zone=zone, 
                 zip_code=zip_code,
                 email=email)

            user.set_password(password)
            user.save()

            return user
    def create_superuser(self, email, password=None):
            if not email:
                raise ValueError('An email is required.')
            if not password:
                raise ValueError('A password is required.')
            
            user = self.create_user(email,password)

            user.is_superuser = True
            user.is_staff = True
            user.save()

            return user
    

class CustomUser(AbstractBaseUser,PermissionsMixin):
    UID = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=4)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=288)
    #profilepic = models.ImageField(upload_to='profile_pictures', default='default.png')



    is_staff=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','province','city','barangay','zone','zip_code']
    objects = AppUserManager()

    def __str__(self):
        return self.email
    
class Sink_Node(models.Model):
     SKID = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
     User = models.ForeignKey(CustomUser,on_delete= models.CASCADE)
     area_address = models.TextField()


class Sensor_Node(models.Model):
     SNID = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
     Sink_Node = models.ForeignKey(Sink_Node,on_delete= models.CASCADE)
     latitude = models.DecimalField(max_digits=9, decimal_places=6)
     longitude = models.DecimalField(max_digits=9, decimal_places=6)

class Readings(models.Model):
     Sensor_Node = models.ForeignKey(Sensor_Node,on_delete=models.CASCADE)
     timestamp = models.DateTimeField()
     latitude = models.DecimalField(max_digits=9, decimal_places=6)
     longitude = models.DecimalField(max_digits=9, decimal_places=6)
     soil_moisture = models.SmallIntegerField()
     temperature = models.SmallIntegerField()
     humidity = models.SmallIntegerField()


