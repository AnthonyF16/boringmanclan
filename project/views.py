from django.shortcuts import render
from django.views.generic import View
from models import *
from django.http import HttpResponse


class LogView(View):
	def post(self, request):
		print request.POST
		return HttpResponse("Success")

	def get(self, request):
		context = {}
		context['entries'] = Entry.objects.all()
		return render(request, 'logs.html', context)


def home(request):
	context = {}
	return render(request, 'index.html', context)