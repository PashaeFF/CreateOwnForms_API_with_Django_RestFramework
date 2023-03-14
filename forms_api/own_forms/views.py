from rest_framework import status
from .models import Form, FilledForms
from rest_framework.response import Response
from rest_framework.decorators import APIView
from .utils.check_auth import authorization
from .utils.helper import check_values_for_add_form, fill_form, filled_form_to_xlsx
from .serializers import FilledFormsSerializer, FormSerializer, CreateValuesSerializer, FillFormSerializer
from rest_framework.pagination import PageNumberPagination
import os, shutil
from drf_yasg.utils import swagger_auto_schema


class FormsAll(APIView):
    @swagger_auto_schema(operation_id="Forms All", tags=['Forms All'])
    def get(self, request):
        forms = Form.objects.all()
        context = {
            'title':'Create your own form',
            'forms': forms.values()
        }
        print(authorization(request))
        return Response({"context":context}, status=status.HTTP_200_OK)
 

class CreateForm(APIView):
    @swagger_auto_schema(operation_id="Create Form", request_body=FormSerializer, tags=['Create New Form'])
    def post(self, request):
        form = request.data
        check_url = Form.objects.filter(url=form['url']).first()
        if check_url:
            return Response({'error':'Url is available'}, status=status.HTTP_409_CONFLICT)
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


class ViewForm(APIView):
    @swagger_auto_schema(operation_id="View Form", tags=['Created Form'])
    def get(self, request, pk=None):
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
            return Response(context, status=status.HTTP_200_OK)
        else:
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)


    @swagger_auto_schema(operation_id="Create Form Values", tags=['Created Form'],
                         operation_description="""{
                            "question_field_1": {
                                        "question_field_1_1_title":"First Title",
                                        "question_field_1_1_description":"Description 1",
                                        "question_field_1_1_image":"https://images.pexels.com/photos/268533/pexels-photo-268533.jpeg?cs=srgb&dl=pexels-pixabay-268533.jpg&fm=jpg",
                                        "question_field_1_1_uploaded_image":"",
                                        "question_field_1_1_youtube":"",
                                        "question_field_1_1_url":"",
                                        "question_field_1_1_button":"button 1",
                                        "question_field_1_2_button":"button 2",
                                        "question_field_1_1_input":"",
                                        "question_field_1_1_values":"",
                                        "question_field_1_1_required":"",
                                        "question_field_1_1_allow":"on",
                                        "question_field_1_1_one_selection":""
                                        }
                                    }""",
                            request_body=CreateValuesSerializer)
    def post(self, request, pk=None):
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


    @swagger_auto_schema(operation_id="Delete Form", tags=['Created Form'])
    def delete(self, request, pk=None):
        form_pk = Form.objects.filter(id=pk).first()
        if form_pk:
            if " " in form_pk.form_name:
                file_name = f'{form_pk.form_name.replace(" ","_")}.xlsx'
            else:
                file_name = f'{form_pk.form_name}.xlsx'
            images_path = f'static/media/{pk}/'
            xlsx_path = 'static/xlsx_files/form/'
            if form_pk:
                Form.objects.filter(id=pk).delete()
                shutil.rmtree(images_path, ignore_errors=True)
                try:
                    os.remove(xlsx_path+file_name)
                except:
                    pass
                message = f'The form with the {form_pk.url} has been deleted'
                return Response({'success':message}, status=status.HTTP_200_OK)
        else:
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)


class GetListForms(APIView):
    @swagger_auto_schema(operation_description="", operation_id="List filled forms", tags=['Filled forms'])
    def get(self, request, pk):
        form_pk = FilledForms.objects.filter(form_id_id=pk).all()
        get_form = Form.objects.filter(id=pk).first()
        if get_form:
            if form_pk:
                context = {
                    'title':get_form.form_name,
                    'id':get_form.id,
                    'url':get_form.url,
                    'author':get_form.fullname,
                }
                serializer_class = FilledFormsSerializer(form_pk, many=True)
                return Response({"context":context, "data":serializer_class.data})
            else:
                message = f'No form has been filled for the "{get_form.form_name}"'
                return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)
        else:
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)


class FillForm(APIView):
    @swagger_auto_schema(operation_id="Fill Form Get", tags=['Form'])
    def get(self, request, pk=None):
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
            return Response(context, status=status.HTTP_200_OK)
        else:
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_204_NO_CONTENT)


    @swagger_auto_schema(operation_id="Fill Form post", tags=['Form'], request_body=FillFormSerializer)
    def post(self, request, pk=None):
        form_pk = Form.objects.filter(id=pk).first()
        #### filled form post request
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


class GetFilledForm(APIView):
    @swagger_auto_schema(operation_id="Filled Form", tags=['Filled forms'])
    def get(self, request, pk=None, wk=None):
        images_path = f'/static/media/{pk}/'
        form_pk = Form.objects.filter(id=pk).first()
        if form_pk:
            filled = FilledForms.objects.filter(id=wk).first()
            if filled:
                filled_form_to_xlsx(request, pk, wk)
                context = {
                    "title":form_pk.form_name,
                    "id":form_pk.id,
                    "url":form_pk.url,
                    "author":form_pk.fullname,
                    "images_path":images_path,
                    "download_xlsx_file":filled_form_to_xlsx(request, pk, wk)
                    }
                form = {}
                for key, value in form_pk.values.items():
                    for key_filled, value_filled in filled.filled_form.items():
                        if key == key_filled:
                            value.update({"answer":value_filled})
                        form.update({key:value})
                if len(filled.filled_form) < 1:
                    message = 'Form is empty'
                    return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
                return Response({"context":context, "form":form} , status=status.HTTP_200_OK)
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
        message = 'Form not found'
        return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
    

class DeleteFilledForm(APIView):
    @swagger_auto_schema(operation_id="Delete Filled Form", tags=['Filled forms'])
    def delete(self, request, wk):
        form_pk = FilledForms.objects.filter(id=wk).first()
        if form_pk:
            if " " in form_pk.fullname:
                file_name = f'{form_pk.fullname.replace(" ","_")}.xlsx'
            else:
                file_name = f'{form_pk.fullname}.xlsx'
            forms_count = Form.objects.filter(id=form_pk.form_id_id).first()
            name = form_pk.fullname
            xlsx_path = f'static/xlsx_files/filled_form/{forms_count.id}/'
            delete_this_form = FilledForms.objects.filter(id=wk)
            delete_this_form.delete()
            Form.objects.filter(id=form_pk.form_id_id).update(forms_count=forms_count.forms_count-1)
            try:
                os.remove(xlsx_path+file_name)
            except:
                pass
            message = f'The form filled by {name} has been deleted'
            return Response({'success':message}, status=status.HTTP_202_ACCEPTED)
        else:
            message = 'Form not found'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)  