from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(unique=True)
  bio = models.TextField(null=True)
  
  avatar = models.ImageField(null=True, default="avatar.svg")
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

class Topic(models.Model):
  name = models.CharField(max_length=200)
  
  def __str__(self) -> str:
    return self.name

class Room(models.Model):
  host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # Topic can have many rooms but rooms can only have one topic.
  
  
  # By default, NULL is not allowed for this column
  # and blank string is also not allowed
  name = models.CharField(max_length=200)
   
  # Allows columns to acceot NULL values in the database,
  # also allows the column to accept blank strings as a value.
  description = models.TextField(null=True, blank=True)
  
  # Creates a many to many relationship between user and room as participants to rooms
  # We use related_name here because we already have a host relationship to rooms that defines
  # the user relationship as a host to the room. To prevent conflicts, we use
  # the related_name so that we can access .participants instead of .room_set
  participants = models.ManyToManyField(User, related_name='participants', blank=True)
  
  # the auto_now True will allow the value of updated
  # column to be updated with the latest time whenever
  # the save method is called. Django will take a timestamp
  # as the value for this column, this is automatically done
  # django already has the value for timestamps built in.
  updated = models.DateTimeField(auto_now=True)
  
  # Difference between auto_now and auto_now_add is that
  # the latter will only update on the first creation for the
  # row of this column.
  created = models.DateTimeField(auto_now_add=True)
  
  class Meta: # naming here is important
    ordering = ['-updated', '-created']
  
  
  def __str__(self) -> str:
    return self.name
  
class Message(models.Model): 
  # One to many relationship, many messages to one room, and to one user
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE) # When parents are deleted, all the messages with FK to that room are deleted
  body = models.TextField()
  
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-updated','-created']
  
  def __str__(self) -> str:
    return self.body[0:50] + "..." if self.body[0:50] != self.body else self.body
