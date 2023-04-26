# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    name = models.TextField(blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    pkey = models.AutoField(primary_key=True, blank=True, null=False)

    class Meta:
        db_table = 'Category'


class Expense(models.Model):
    amount = models.IntegerField(blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    expense_date = models.TextField(blank=True, null=True)
    added_date = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    pkey = models.AutoField(primary_key=True, blank=True, null=False)

    class Meta:
        db_table = 'Expense'
