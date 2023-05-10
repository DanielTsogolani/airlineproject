# models.py

from django.db import models

from django.utils import timezone

class Airline(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='airline_logo/', null=True, blank=True)
    website = models.URLField()


    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Aircraft(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    registration = models.CharField(max_length=20)
    accumulated_hours = models.IntegerField(default=0)
    inspection_requirement = models.ForeignKey('InspectionRequirement', on_delete=models.CASCADE)

    def __str__(self):
        return self.registration
    
    def is_due_for_inspection(self):
        last_inspection_date = self.inspection_requirement.last_inspection_date
        threshold_hours = self.inspection_requirement.threshold_hours
        hours_since_inspection = self.accumulated_hours - self.inspection_requirement.last_inspection_hours
        
        if hours_since_inspection >= threshold_hours:
            return True
        else:
            return False

class InspectionRequirement(models.Model):
    aircraft_type = models.CharField(max_length=50)
    threshold_hours = models.IntegerField(default=0)
    last_inspection_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.aircraft_type

class Pilot(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    total_hours_flown = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    departure_airport = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f'{self.flight_number} - {self.departure_airport} to {self.arrival_airport}'
