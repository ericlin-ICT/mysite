from django.shortcuts import render

# Create your views here.


from mysite.tables.models import Person

def people(request):
  return render(request, "people.html", {"people": Person.objects.all()})