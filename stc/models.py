from django.db import models
from django.contrib.auth.models import User

class user(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    gender_choices = (
        ('MALE', 'male'),
        ('FEMALE', 'female'),
        ('OTHERS', 'others'),
    )
    gender = models.CharField(choices=gender_choices, max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='userimg/', null=True, blank=True)
    phonenumber = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True)
    from_address = models.CharField(max_length=255, blank=True)
    to_address = models.CharField(max_length=255, blank=True)
    def __str__(self):
         return self.email 
    
class rto(models.Model):
     fullname=models.CharField(max_length=100,unique=True)
     email=models.EmailField(unique=True)
     phonenumber=models.IntegerField()
     stationplace_choice=(
          ('THRISSUR','thrissur (KL-08)'),
		('ALAPPUZHA','alappuzha (KL-04)'),
	     ('ATTINGAL','attingal (KL-16)') ,
          ('ERANAKULAM','ernakulam (KL-07)'),
          ('IDUKKI','idukki (KL-06)'),
          ('KANNUR','kannur (KL-13)'),
          ('KASARGOD','kasaragod (KL-14)'),
          ('KOLLAM','kollam (KL-02)'),
          ('KOTTAYAM','kottayam (KL-05)'),
          ('KOZHIKODE','kozhikode (KL-11)'),

     )
     createpassword=models.CharField(max_length=150)
     repeatepassword=models.CharField(max_length=150)
     rtoimage=models.ImageField(upload_to='rtoimage/',null=True,blank=True)



class Feedback(models.Model):
     RATING_CHOICES = [
          (1, '1'),
          (2, '2'),
          (3, '3'),
          (4, '4'),
          (5, '5'),                          
 ]
     feedback_text = models.TextField() 
     rating = models.IntegerField(choices=RATING_CHOICES) 
     created_at = models.DateTimeField(auto_now_add=True) 
     email=models.EmailField()
     def _str_(self):
          return f"Rating: {self.rating}, feedback: {self.feedback_text[:50]}..."
     
class Wallet(models.Model):
     wuser=models.ForeignKey(user,on_delete=models.CASCADE)
     amount= models.DecimalField(max_digits=300,decimal_places=4)
     created_at= models.DateTimeField(auto_now=True)
     is_paid=models.BooleanField(default=False)

     def __str__(self):
        return f"{self.wuser.name or 'Unnamed User'} - Wallet Balance: ₹{self.amount}"
     
class BusRoute(models.Model):
    route_name = models.CharField(max_length=150)  # Example: "Route A - Downtown to City Center"
    start_point = models.CharField(max_length=150)
    end_point = models.CharField(max_length=150)
    fare = models.DecimalField(max_digits=10, decimal_places=2)  # Fare for the route
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.route_name} ({self.start_point} - {self.end_point})"
    
class BusConductor(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    email= models.EmailField(max_length=50,null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    password= models.CharField(max_length=50,null=True,blank= True)
    busname= models.CharField(max_length=50,null=True,blank=True)
    photo=models.ImageField(upload_to='conductor_image/',null=True,blank=True)


from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode

class BusPass(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.ImageField(upload_to='bus_pass_qr/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)  # Number of times the ticket has been used
    max_usage = models.IntegerField(default=2)

    def generate_qr_code(self):
        data = f"User: {self.user.email}, From: {self.from_address}, To: {self.to_address}, Amount: {self.amount}"
        qr = qrcode.make(data)
        buffer = BytesIO()
        qr.save(buffer, 'PNG')
        buffer.seek(0)
        self.qr_code.save(f"{self.user.id}_bus_pass.png", ContentFile(buffer.read()), save=False)

class Transaction(models.Model):
    bus_pass = models.ForeignKey(BusPass, on_delete=models.CASCADE)
    conductor = models.ForeignKey(BusConductor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
