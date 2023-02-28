from rest_framework import status, generics
from .models import Form, FilledForms
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils.helper import check_values_for_add_form, fill_form

class FormsView(generics.GenericAPIView):
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


    @api_view(('GET','POST'))
    def get_form(request, pk=None):
        form_pk = Form.objects.filter(id=pk).first()
        images_path = f'/static/media/{pk}/'
        if form_pk:
            values = form_pk.values
            if len(values) < 1:
                message = 'The form is empty, fill in your information'
                return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)
            context = {
                'title':form_pk.form_name,
                'id':form_pk.id,
                'url':form_pk.url,
                'author':form_pk.fullname,
                'images_path':images_path,
                'data':values
            }
            #### filled form post request
            if request.method == 'POST':
                if 'email' in request.data.keys():
                    email = request.data['email']
                    if len(email) < 4 or "@" not in email:
                        message = 'Wrong email'
                        return Response({'error':message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    message = 'Enter your email address'
                    return Response({'error':message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                if 'fullname' in request.data.keys():
                    fullname = request.data['fullname']
                    if len(fullname) < 1:
                        message = 'Enter your name'
                        return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)
                else:
                    message = 'Enter your name'
                    return Response({'error':message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                FilledForms.objects.create(email=email, fullname=fullname, filled_form=fill_form(request, pk, form_pk), form_id_id=form_pk.id)
                Form.objects.filter(id=form_pk.id).update(forms_count=form_pk.forms_count+1)
                message = 'Form filled successfull'
                return Response({'success':message}, status=status.HTTP_201_CREATED)
            return Response(context, status=status.HTTP_200_OK)
        else:
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)
        

    @api_view()
    def get_the_list_of_filled_form(request, pk=None):
        form_pk = FilledForms.objects.filter(form_id_id=pk).all()
        get_form = Form.objects.filter(id=pk).first()
        if form_pk:
            context = {
                'title':get_form.form_name,
                'id':get_form.id,
                'url':get_form.url,
                'author':get_form.fullname,
            }
            filled_list = []
            for item in form_pk:
                filled_list.append({
                    "id":item.id,
                    "email":item.email,
                    "filled_form":item.filled_form,
                    "created_at":item.created_at.strftime('%Y-%m-%d %H:%M'),
                    })
            return Response({"context":context, "filled_list":filled_list}, status=status.HTTP_200_OK)
        else:
            message = f'No form has been filled for the "{get_form.form_name}"'
            return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)
        

    @api_view()
    def get_filled_form(request, pk=None, wk=None):
        images_path = f'/static/media/{pk}/'
        form_pk = Form.objects.filter(id=pk).first()
        if form_pk:
            filled = FilledForms.objects.filter(id=wk).first()
            if filled:
                # filled_form_to_xlsx(request, pk, wk)
                context = {
                "title":form_pk.form_name,
                "id":form_pk.id,
                "url":form_pk.url,
                "author":form_pk.fullname,
                "images_path":images_path
                }
                form = {}
                for key, value in form_pk.values.items():
                    for key_filled, value_filled in filled.filled_form.items():
                        if key == key_filled:
                            value.update({"answer":value_filled})
                        form.update({key:value})
                if len(filled.filled_form) < 1:
                    message = 'Form is empty'
                    return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)
                return Response({"context":context, "form":form} , status=status.HTTP_200_OK)
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)
        message = 'Form not found'
        return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)