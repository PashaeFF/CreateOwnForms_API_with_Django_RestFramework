from django.shortcuts import render
from rest_framework import generics, status
from .models import Form, FilledForms
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils.helper import check_values_for_add_form


@api_view(('GET','POST'))
def index(request):
    forms = Form.objects.all()
    context = {
        'title':'Create your own form',
        'forms': forms.values()
    }
    if request.method == 'POST':
        form = request.data
        check_url = Form.objects.filter(url=form['url']).first()
        print(check_url)
        if check_url:
            Response({'error':'Url is available'}, status=status.HTTP_409_CONFLICT)
        else:
            new_form = Form.objects.create(email=form['email'], url=form['url'],
                                            fullname=form['fullname'], form_name=form['form_name'])
            new_form.save()
            return Response({'created':{
                            'Email':form['email'],
                            'Url':form['url'],
                            'Fullname':form['fullname'],
                            'Form name':form['form_name']
                        }}, status=status.HTTP_201_CREATED)
    return Response(context, status=status.HTTP_200_OK)


@api_view(('GET','POST'))
def create_values_for_form(request, pk=None):
    form_pk = Form.objects.filter(id=pk).first()
    files_path = f'/static/'
    if form_pk:
        context = {
            'title':form_pk.form_name,
            'url':form_pk.url,
            'author':form_pk.fullname,
            'files_path':files_path
        }
        if request.method == 'POST':
            if 'message' in check_values_for_add_form(request, pk, form_pk).keys():
                return Response(check_values_for_add_form(request, pk, form_pk)['message'], status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                Form.objects.filter(id=pk).update(values=check_values_for_add_form(request, pk, form_pk))
                return Response({'success':'Form created'}, status=status.HTTP_201_CREATED)
        return Response(context, status=status.HTTP_200_OK)
    else:
        return Response({'error':'Form not found'}, status=status.HTTP_404_NOT_FOUND)
    
