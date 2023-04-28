# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Observations(models.Model):
    observation_id = models.AutoField(primary_key=True)
    observer_id = models.IntegerField(blank=True, null=True)
    species_id = models.IntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Observations'


class Observers(models.Model):
    observer_id = models.AutoField(primary_key=True)
    observer_name = models.TextField(blank=True, null=True)
    observer_email = models.TextField(blank=True, null=True)
    observation_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Observers'


class Russianbirds(models.Model):
    species_id = models.AutoField(primary_key=True)
    species_name = models.TextField()
    genus_name = models.TextField(blank=True, null=True)
    latin = models.TextField(blank=True, null=True)
    habitat = models.TextField(blank=True, null=True)
    observation_number = models.IntegerField(blank=True, null=True)
    aka = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RussianBirds'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
