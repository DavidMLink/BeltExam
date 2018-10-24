from __future__ import unicode_literals
from django.db import models
from datetime import datetime

now = str(datetime.now())

# VALIDATION
class UserManager(models.Manager):
    def basic_validator(self, postData):
        print("POSTDATA is", postData)
        errors = {}
        if len(postData["full_name"]) < 3:
            errors["full_name"] = "Name must be at least 3 characters"
        if len(postData["username"]) < 3:
            errors["username"] = "Username must be at least 3 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Password and confirm password do NOT match!'
        return errors

    def login_validator(self, postData):
        print("POSTDATA is", postData)
        errors = {}
        if not User.objects.filter(username = postData["username"]):
            errors["username"] = "Uhm, this username was not found, please register!"
        return errors

class PlanManager(models.Manager):
    def basic_validator(self, postData):
        print("POSTDATA is", postData)
        errors = {}
        if len(postData["destination"]) < 1:
            errors["destination"] = "Destination is required"
        if len(postData["start_date"]) < 1:
            errors["start_date"] = "Start Date is required"
        if len(postData["end_date"]) < 1:
            errors["end_date"] = "End Date is required"
        if postData["start_date"] > postData["end_date"]:
            errors['start_date'] = "End Date must be after start date!"
        if postData['start_date'] < now:
            errors["start_date"] = "Start Date must be a future date!"
        if len(postData["description"]) < 1:
            errors["description"] = "Description is required"
        return errors
#END OF VALIDATION


# TABLES

class User(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Plan(models.Model):

    #ONE TO MANY RELATIONSHIP
    added_by = models.ForeignKey(User, related_name="plans", on_delete = models.CASCADE)

    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = PlanManager()

#MANY TO MANY RELATIONSHIP
class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="user_favorites", on_delete = models.CASCADE)
    plan = models.ForeignKey(Plan, related_name="plan_favorites", on_delete = models.CASCADE)

# END OF TABLES
