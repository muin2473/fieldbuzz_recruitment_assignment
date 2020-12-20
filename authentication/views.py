import redis
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

cache_ttl = getattr(settings, "TTL")
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST or 'localhost', port=settings.REDIS_PORT, db=0)


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
	prev_token = redis_instance.get("Token")
	if prev_token is not None:
		return redirect('/recruitmentinformation/')
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			# Authenticate user
			url = "https://recruitment.fisdev.com/api/login/"
			payload = {"username": username, "password": password}
			response = requests.post(url, data=payload)

			if response.status_code == 200:
				data = response.json()
				redis_instance.set("Token", data["token"], ex=cache_ttl)

				return redirect('/recruitmentinformation/')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="authetication/login.html", context={"form": form})
