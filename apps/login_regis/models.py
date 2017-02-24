from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

email_valid = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
name_valid = r'^[a-zA-Z]{3,}$'
pass_valid = r'^[a-zA-Z0-9.+_-]{8,}$'
entry_valid = r'^[a-zA-Z0-9.+_-]{1,}$'


class UserManager(models.Manager):

    def login(self, logData):
        no_errors = True
        login_errors =[]
        # result = no_errors, login_errors
        try:
            username = User.objects.get(username=logData["username_login"].lower())
            if bcrypt.hashpw(logData["password_login"].encode(), username.password.encode()) == username.password:
                result = no_errors, login_errors, username.id
            else:
                no_errors = False
                login_errors.append("Password does not Match")
                result = no_errors, login_errors


        except:
            no_errors = False
            login_errors.append("User does not exist")
            result = no_errors, login_errors

        return result


    def register(self, postData):
        no_errors = True
        error_messages =[]
        if re.match(email_valid, postData["email"]):
            print "valid email"
            try:
                User.objects.get(email=postData["email"])
                no_errors = False
                error_messages.append("Email address already in use")
            except:
                print "New user"
        else:
            no_errors = False
            error_messages.append("Invalid Email Address")



        if re.match(name_valid, postData["name"]):
            print "valid Name"
            try:
                User.objects.get(name=postData["name"])
                no_errors = False
                error_messages.append("Name already in use")
            except:
                print "New Name"
        else:
            no_errors = False
            error_messages.append("Invalid Name, please enter 3 or more Letters")



        if re.match(name_valid, postData["username"]):
            print "valid Username"
            try:
                User.objects.get(username=postData["username"])
                no_errors = False
                error_messages.append("Username already in use")
            except:
                print "New Username"
        else:
            no_errors = False
            error_messages.append("Invalid Username, please enter 3 or more Letters")


        if re.match(pass_valid, postData["password"]):
            print "valid Password"
        else:
            no_errors = False
            error_messages.append("Invalid Password, please enter 8 or more characters")
        if postData["password"]== postData["confirm"]:
            print "Password Confirmed"
        else:
            no_errors = False
            error_messages.append("Password confirmation did no match")
        if no_errors:
            hashed = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            User.objects.create(name=postData["name"].lower(), username=postData["username"].lower(), email=postData["email"].lower(), password=hashed)

        return no_errors, error_messages

    def add_trip(self, addData):
        no_errors = True
        add_errors = []
        if re.match(entry_valid, addData["destination"]):
            print "valid destination"
        else:
            no_errors = False
            add_errors.append("Please enter a valid destination of 1 character or more")
            trip_result = no_errors, add_errors
        if re.match(entry_valid, addData["description"]):
            print "Valid description"
        else:
            no_errors = False
            add_errors.append("Please enter a valid description of 1 character or more")
            trip_result = no_errors, add_errors
        if re.match(entry_valid, addData["travel_from"]):
            print "Valid Travel Date From"
        else:
            no_errors = False
            add_errors.append("Please enter a valid Travel Date From")
            trip_result = no_errors, add_errors
        if re.match(entry_valid, addData["travel_to"]):
            print "Valid Travel Date To"
        else:
            no_errors = False
            add_errors.append("Please enter a valid Travel Date To")
            trip_result = no_errors, add_errors
        if no_errors:
            Travel.objects.create(location=addData["destination"].lower(), description=addData["description"], travel_from=addData["travel_from"], travel_to=addData["travel_to"])
            destination = Travel.objects.get(location=addData["destination"].lower())
            trip_result = no_errors, add_errors, destination.id
        return trip_result
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return "email: {}".format(self.email)

class Travel(models.Model):
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_from = models.CharField(max_length=255)
    travel_to = models.CharField(max_length=255)
    # travel_from = models.DateField('%m/%d/%Y')
    # travel_to = models.DateField('%m/%d/%Y')
    trips = models.ManyToManyField(User, related_name="Group")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return "location: {}".format(self.location)
