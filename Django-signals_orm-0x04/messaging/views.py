from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    request.user.delete()
    return HttpResponse("User deleted!")
    
