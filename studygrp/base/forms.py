from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['name', 'username', 'email', 'password1', 'password2', 'bio']

class RoomForm(ModelForm):
  class Meta:
    model = Room
    fields = '__all__' # Creates a form based on all the attributes of the Room class, except those non editable fields such as updated and created
    exclude = ['host', 'participants']

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['avatar', 'name', 'username', 'email', 'bio']
        
