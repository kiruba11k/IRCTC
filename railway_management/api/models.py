from django.db import models
from django.contrib.auth.models import User
from datetime import time, date
from django.utils import timezone


class Train(models.Model):
    DAILY = 'Daily'
    EVERY_TWO_DAYS = 'Every two days'

    SCHEDULE_CHOICES = [
        (DAILY, 'Daily'),
        (EVERY_TWO_DAYS, 'Every two days'),
    ]
    ALL='All'
    SLEEPER = 'Sleeper'
    UPPER_BERTH = 'Upper Berth'
    LOWER_BERTH = 'Lower Berth'
    AC_COACH = 'AC Coach'

    SECTION_CHOICES = [
        (ALL,'All'),
        (SLEEPER, 'Sleeper'),
        (UPPER_BERTH, 'Upper Berth'),
        (LOWER_BERTH, 'Lower Berth'),
        (AC_COACH, 'AC Coach'),
    ]
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()
    arrival_time = models.TimeField(default=time(0, 0))  
    departure_time = models.TimeField(default=time(0, 0))  
    date = models.DateField(default=date.today)  
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, default=DAILY)
    sections = models.JSONField(default=dict)  

    def __str__(self):

        return f"{self.name} ({self.source}  {self.arrival_time} - {self.destination} {self.departure_time})"
    

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    train=models.ForeignKey(Train,on_delete=models.CASCADE)
    seats_booked=models.PositiveIntegerField()
    section= models.CharField(max_length=20, choices=Train.SECTION_CHOICES,default=Train.ALL)

    
    def __str__(self):
        return f"Booking by {self.user.username} on {self.train.name} in {self.section}"
    
class AdminAPIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s API Key"
    


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=100)
    train_id = models.IntegerField()
    section = models.CharField(max_length=50)
    seat_number = models.IntegerField()
    train_arrival = models.DateTimeField()
    train_departure = models.DateTimeField()
    booking_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Booked')

    def __str__(self):
        return f"Ticket #{self.ticket_id} - {self.train_name} ({self.section}), Seat {self.seat_number} - {self.user.username}"
