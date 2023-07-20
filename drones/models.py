from django.db import models

class DroneCategory(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"])
        ]
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Drone(models.Model):
    name = models.CharField(max_length=250, unique=True)
    drone_category = models.ForeignKey(DroneCategory, related_name="drones", on_delete=models.CASCADE)
    manufacturing_date = models.DateTimeField()
    has_it_competed = models.BooleanField(default=False)
    inserted_timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='drones', on_delete=models.CASCADE)


    class Meta:
        indexes = [models.Index(fields=['name'])]
        ordering = ('name',)

    def __str__(self):
        return self.name

class Pilot(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female")
    )
    name = models.CharField(max_length=150, blank=False, unique=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=MALE)
    races_count = models.PositiveIntegerField()
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=['-name'])]
        ordering = ("-inserted_timestamp",)

    def __str__(self):
        return self.name

class Competition(models.Model):
    pilot = models.ForeignKey(Pilot, related_name='competitions', on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, related_name='competitions', on_delete=models.CASCADE)
    distance_in_feet = models.IntegerField()
    distance_achievement_date = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["-distance_in_feet"])]
        ordering = ['-distance_in_feet']

    def __str__(self):
        return self.pilot.name - self.drone.name