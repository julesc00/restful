from django.db import models


GENDERS = (
    ("M", "Male"),
    ("F", "Female"),
)


class DroneCategory(models.Model):
    """Create the drone_category object."""
    name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Drone(models.Model):
    """Create the drone object."""
    name = models.CharField(max_length=150)
    drone_category = models.ForeignKey(DroneCategory, related_name="drones", on_delete=models.CASCADE)
    manufacturing_date = models.DateTimeField(blank=True)
    competed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Pilot(models.Model):
    """Create the pilot object."""
    name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, default="M")
    races_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Competition(models.Model):
    """Create the competition object."""
    pilot = models.ForeignKey(Pilot, related_name="competitions", on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    distance_in_feet = models.FloatField(default=0)
    distance_achievement_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-distance_in_feet",)

    def __str__(self):
        return str(f"{self.distance_in_feet} ft.")

