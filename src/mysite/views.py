from django.http import HttpResponse
from django.http import Http404
from django.template import Context
#from django.template import Template
#from django.template.loader import get_template
from django.shortcuts import render_to_response
from mysite.books.models import Book
import datetime
from django import forms
import random
import os
from django.http.response import HttpResponse
from mysite.load_data import load_data

def hello(request):
	return HttpResponse("Hello World")

def current_datetime(request):
	now = datetime.datetime.now()
	#t = get_template('current_datetime.html')
	#html = t.render(Context({'current_date' : now}))
	c = Context( {'current_date': now} )
	return render_to_response('current_datetime.html', c)

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()

	assert False

	#dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	#html = "<html><body>In %s hour(s), it will be %s. </body></html>" % (offset, dt)
	return HttpResponse


def display_request_info(request):
	values = request.META.items()
	values.sort()
	html = []
	for k, v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))

	return HttpResponse('<table>%s</table>' % '\n'.join(html))

def display_request_info_tpl(request):
	values = request.META.items()
	values.sort()
	c = Context({'item_list' : values})
	return render_to_response('meta_info.html', c)


def search_form(request):
	return render_to_response('search_form.html')

def search(request):
	error = False
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			error = True
		else:
			books = Book.objects.filter(title__icontains=q)
			return render_to_response('search_results.html',
					{'books':books, 'query':q})
	
	return render_to_response('search_form.html',
			{'error':error})

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file  = forms.FileField()
	
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			path = os.path.join(os.path.dirname(__file__),'media/%s'%request.FILES['file'])
			data = load_data(path)
			return HttpResponse(str(data))
	else:
		form = UploadFileForm()
	return render_to_response('upload_result.html', {'form': form}) 
 
def handle_uploaded_file(f):
	path = os.path.join(os.path.dirname(__file__),'media/%s'%f)
	destination = open(path, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.flush()
	destination.close()
   