import time
import redis
import uuid
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import InformationForm

cache_ttl = getattr(settings, "TTL")
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST or 'localhost', port=settings.REDIS_PORT, db=0, decode_responses=True)
current_milli_time = lambda: int(round(time.time() * 1000))


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
	if request.method == "POST":
		form = InformationForm(request.POST, request.FILES)
		if form.is_valid():
			tsync_id = uuid.uuid1()
			name = form.cleaned_data.get('name')
			email = form.cleaned_data.get('email')
			phone = form.cleaned_data.get('phone')
			full_address = form.cleaned_data.get('full_address')
			name_of_university = form.cleaned_data.get('name_of_university')
			graduation_year = form.cleaned_data.get('graduation_year')
			cgpa = form.cleaned_data.get('cgpa')
			experience_in_months = form.cleaned_data.get('experience_in_months')
			current_work_place_name = form.cleaned_data.get('current_work_place_name')
			applying_in = form.cleaned_data.get('applying_in')
			applying_in = dict(form.fields['applying_in'].choices)[applying_in]
			expected_salary = form.cleaned_data.get('expected_salary')
			field_buzz_reference = form.cleaned_data.get('field_buzz_reference')
			github_project_url = form.cleaned_data.get('github_project_url')
			cv_file = request.FILES['cv_file']
			cv_file_tsynnc_id = uuid.uuid1()

			# Request to API
			url = "https://recruitment.fisdev.com/api/v1/recruiting-entities/"
			payload = {
				"tsync_id": str(tsync_id),
				"name": str(name),
				"email": str(email),
				"phone": str(phone),
				"full_address": str(full_address),
				"name_of_university": str(name_of_university),
				"graduation_year": int(graduation_year),
				"cgpa": float(cgpa),
				"experience_in_months": int(experience_in_months),
				"current_work_place_name": str(current_work_place_name),
				"applying_in": str(applying_in),
				"expected_salary": int(expected_salary),
				"field_buzz_reference": str(field_buzz_reference),
				"github_project_url": str(github_project_url),
				"cv_file": {
					"tsync_id": str(cv_file_tsynnc_id)
				},
				"on_spot_update_time": current_milli_time(),
				"on_spot_creation_time": current_milli_time()
			}

			token = "Token " + redis_instance.get("Token")
			headers = {"Authorization": token}
			response = requests.post(url, json=payload, headers=headers)

			if response.status_code == 201:
				data = response.json()
				file_token_id = data["cv_file"]["id"]
				file_url = "https://recruitment.fisdev.com/api/file-object/" + str(file_token_id) + "/"
				headers = {"Authorization": token}
				files = {'file': ('resume.pdf', cv_file)}
				response = requests.put(file_url, files=files, headers=headers)
				if response.status_code == 200:
					return Response(response.json(), status=status.HTTP_200_OK)
				else:
					messages.error(request, "Upload file error")
			else:
				print("Invalid")
				messages.error(request, "Invalid response")

		else:
			print("not valid")
			messages.error(request, "Invalid data")

	form = InformationForm()
	return render(request=request, template_name='recruitmentinformation/information.html', context={'form': form})
