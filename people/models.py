from django.db import models


class Person(models.Model):
    """An individual Person"""
    name = models.TextField()
    site = models.ForeignKey("Site", on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return self.name


class Observatory(models.Model):
    """e.g. Green Bank Observatory, NRAO"""
    name = models.TextField()

    def __str__(self):
        return self.name


class Site(models.Model):
    """e.g. Green Bank, Charlottesville, Socorro"""
    name = models.TextField()
    observatory = models.ForeignKey("Observatory", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
