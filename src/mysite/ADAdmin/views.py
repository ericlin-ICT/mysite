#-*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django import forms
import os
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from tarfile import pwd
from clouddesktop.util import load_data
from django.core.files.uploadedfile import InMemoryUploadedFile
from pandas.core.frame import DataFrame
from django.http.request import QueryDict
from clouddesktop.core.query import AsyncQuery
from clouddesktop.core.add import Add

# Create your views here.

class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file  = forms.FileField()
  
def handle_uploaded_file(f):
  #print 'f.name type', type(f.name)
  store_path = os.path.join(os.path.dirname(__file__),'media/%s' % f.name)
  #print store_path
  destination = open(store_path, 'wb+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.flush()
  destination.close()  
  print 'upload finished'
  return store_path
  
'''
def upload_file(request):
  if request.method == 'POST':
    file_name  = request.FILES['file_name']
    server     = request.POST['server']
    port       = int(request.POST['port'])
    user_email = request.POST['user_email']
    pwd        = request.POST['password']
    dc         = request.POST['dc']
    
    store_path = handle_uploaded_file(file_name)
    print type(port)
    data = load_data.load_data(store_path, server, port, user_email, pwd, dc)
    text = '<html><table>'
    for record in data:
      text += ('<tr>')
      for col in record:
        text += ('<td>')
        text += str(col)
        text += ('</td>')
      text += ('</tr>')
    text += ('</table><input name="submit" type="submit"></html>')
    return HttpResponse(text)
  else:
    return render_to_response('upload_excel.html') 
'''
def upload_file(request):
  if request.method == 'POST':
    file_name  = request.FILES['file_name']
    server     = request.POST['server']
    port       = int(request.POST['port'])
    user_email = request.POST['user_email']
    pwd        = request.POST['password']
    dc         = request.POST['dc']
    request.session['server'] = server
    request.session['port'] = port 
    request.session['user_email'] = user_email 
    request.session['pwd'] = pwd 
    request.session['dc'] = dc 
    
    store_path = handle_uploaded_file(file_name)
    print type(port)
    data = load_data.load_data(store_path, server, port, user_email, pwd, dc)
    request.session['data'] = data
    return render_to_response('analysis_result.html', {'res_data': data}) 
  else:
    return render_to_response('upload_excel.html')
  

def process(request):
  if request.method == 'POST':
    server = request.session['server']  
    port = int(request.session['port'])   
    user_email = request.session['user_email']   
    pwd = request.session['pwd']   
    dc = request.session['dc']   
    data = request.session['data']
    adder = Add(server,user_email,pwd,dc,port)
    query = AsyncQuery(server, user_email, pwd, dc, port)
    result = []
    for record in data:
      print record
      logon_name = record[3]
      gp_lst = record[14]
      flag = record[15]
      print logon_name, gp_lst, record[14]
      if flag == 'Good':
        print 'good'
        user_dn = query.async_get_dn(logon_name)
        res = logon_name + '添加组： '
        for gp in gp_lst:
          gp_dn = query.async_get_dn(gp)
          print user_dn, gp_dn
          adder.add_group(gp_dn, user_dn)
          res = res + gp + ' '
        result.append(res)
      if flag == 'Duplicate group':
        res = logon_name + '已有该组资源，不予操作！'
        result.append(res)
      if flag == 'No User':
        res = logon_name + '用户不存在，请flpm就绪后再申请'
        result.append(res)
    
    return render_to_response('result.html', {'result':result})
  else:
    return HttpResponse('get 错啦！')