from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True)
    pump_name = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.phone)+"]["+str(self.pump_name)+"]["+str(self.address)+"]"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.phone)+"]"

class Employee(models.Model):
    emp_no = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=50)
    hire_date = models.CharField(max_length=50)
    salary = models.IntegerField()
    password = models.CharField(max_length=50)
    image = models.ImageField(upload_to="", blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return "["+str(self.emp_no)+"]["+str(self.first_name)+"]["+str(self.last_name)+"]["+str(self.gender)+"]["+str(self.phone)+"]["+str(self.email)+"]["+str(self.address)+"]["+str(self.birth_date)+"]["+str(self.hire_date)+"]["+str(self.password)+"]["+str(self.salary)+"]["+str(self.owner)+"]"

class Supplier(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    def __str__(self):
        return "["+str(self.first_name)+"]" + "["+str(self.last_name)+"]["+str(self.phone)+"]["+str(self.email)+"]["+str(self.owner)+"]"

class Machine(models.Model):
    machine_no = models.CharField(max_length=50, primary_key=True)
    machine_type = models.CharField(max_length=100)
    machine_company = models.CharField(max_length=100)
    machine_desc = models.CharField(max_length=500)
    machine_price = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    def __str__(self):
        return "["+str(self.machine_no)+"]" + "["+str(self.machine_type)+"]["+str(self.machine_company)+"]["+str(self.machine_desc)+"]["+str(self.machine_price)+"]["+str(self.owner)+"]"

class Slot(models.Model):
    slot_date = models.CharField(max_length=50)
    slot_time = models.CharField(max_length=50)
    slot_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pending')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return "["+str(self.slot_date)+"]" + "["+str(self.slot_time)+"]["+str(self.owner)+"]["+str(self.customer)+"]"

class Feedback(models.Model):
    feedback_date = models.DateField(max_length=50, default=datetime.now())
    feedback_message = models.CharField(max_length=500)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return "["+str(self.feedback_date)+"]" + "["+str(self.feedback_message)+"]["+str(self.owner)+"]["+str(self.customer)+"]"

class PUC(models.Model):
    vehicle_no = models.CharField(max_length=20)
    date_of_apply = models.DateField(default=datetime.now())
    date_of_issue = models.DateField(blank=True, null=True, default=None)
    date_of_expiry = models.DateField(blank=True, null=True, default=None)
    carbon_monoxide = models.FloatField(default=0.0)
    hydro_carbon = models.FloatField(default=0.0)
    methane_hc = models.FloatField(default=0.0)
    reactive_hc = models.FloatField(default=0.0)
    charges = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default='Pending')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return "["+str(self.vehicle_no)+"]" + "["+str(self.date_of_apply)+"]["+str(self.date_of_issue)+"]["+str(self.date_of_expiry)+"]["+str(self.carbon_monoxide)+"]["+str(self.hydro_carbon)+"]["+str(self.methane_hc)+"]["+str(self.reactive_hc)+"]["+str(self.charges)+"]["+str(self.status)+"]["+str(self.owner)+"]["+str(self.customer)+"]"
