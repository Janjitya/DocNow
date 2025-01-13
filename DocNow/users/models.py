from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Profile(models.Model):

    GENDER = {
        "Male": "MALE",
        "Female": "FEMALE",
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, default="media/users/upload_area.png")
    address1 = models.CharField(max_length=300, null=True)
    address2 = models.CharField(max_length=200, null=True)
    phone    = models.IntegerField(null=True)
    gender = models.CharField(choices=GENDER, max_length=50, null=True)

    def __str__(self): 
        return self.user.username 
    
class Doctor(models.Model):

    SPECIALITY = {
        "General Physician": "General Physician",
        "Gynecologist": "Gynecologist",
        "Dermatologist": "Dermatologist",
        "Paediatrician": "Paediatrician",
        "Neurologist" : "Neurologist",
        "Gastroenterologists" : "Gastroenterologists"
    }
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    speciality = models.CharField(choices=SPECIALITY, max_length=200)
    degree = models.CharField(max_length=200)
    experience = models.IntegerField()
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    fees = models.IntegerField()
    about = models.TextField(max_length=500)
    photo = models.ImageField(upload_to='users/doctors/%Y/%m/%d')
    slug = models.SlugField(max_length=200)
    password = models.CharField(max_length=128)
    
    def set_password(self, raw_password):
        self.password = raw_password
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
class Appiontment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled','Cancelled'),
    ]
       

    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='doctor', on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    

    def __str__(self):
        return f"{self.patient.first_name} - {self.appointment_date}"