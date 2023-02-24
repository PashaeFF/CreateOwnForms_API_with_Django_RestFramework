from rest_framework import status
from ..models import Form, FilledForms
from rest_framework.response import Response
from .image_check_and_upload import check_image_upload_errors, image_upload


def check_values_for_add_form(request, pk, form_pk):
    form_keys = ['checkbox_field', 'question_field']
    ### Dict to add to the database
    my_dict = {}
    form = request.data
    count = 0
    if len(form) < 1:
        message = 'Form is empty'
        return {'message':{'error':message}}
    for f_key, add in form.items():
        # print("key: ",k, "Value: ",add)
        f_key_parts = f_key.split("_")
        for nums, (key, add_item )in enumerate(add.items(), 1):
            # print(key,add_item)
            # print(k)
            key_parts = key.split("_")
            # print("parts>>>", key_parts)
            #### Index 0 of the dict is set to 'title'. A title must be included. Returns an error if 'header' is missing or has been modified
            if nums == 1:
                if key_parts[-1] != 'title':
                    message = 'Title has not been added'
                    return {'message':{'error':message}}
            # #### We compare this (field_name) to a list of 'form_keys' so that other keys in the frontend are not located in the database
            field_name = "_".join(key_parts[:3])
            # print("field_name", field_name)
            field_check_name = "_".join(f_key_parts[:2])
            if key_parts[-1] == 'description':
                if len(add_item) == 0:
                    continue
            # if len(add_item) < 1:
            #     message = 'Inputs cannot be empty'
            #     return {'message':{'error':message}}
            if field_check_name not in form_keys:
                message = 'Something went wrong'
                return {'message':{'error':message}}
            if f_key not in my_dict:
                my_dict[f_key] = {'title':None,'description':None,'image':[],'uploaded_image':[],'youtube':[],
                                        'url':[],'button':[],'input':None,'values':[], 'required':None, 'allow':None, 'one_selection':None, 'counter':0}               
            ######## check dictionary keys
            if field_check_name == 'question_field':
                if key_parts[-1] == 'button':
                    my_dict[f_key]['button'].append(add_item)
                if key_parts[-1] == 'allow':
                    my_dict[f_key].update({'allow':True})
                my_dict[f_key].update({'input':True})
            if key_parts[-1] == 'title':
                my_dict[f_key].update({'title':add_item})
                count+=1
                my_dict[f_key].update({'counter':count})
            elif key_parts[-1] == 'description':
                my_dict[f_key].update({'description':add_item})
            elif key_parts[-1] == 'image':
                my_dict[f_key].get('image').append(add_item)
            elif key_parts[-1] == 'youtube':
                my_dict[f_key].get('youtube').append(add_item)
            elif key_parts[-1] == 'url':
                my_dict[f_key].get('url').append(add_item)
            elif key_parts[-1] == 'values':
                my_dict[f_key].get('values').append(add_item)
            elif key_parts[-1] == 'select':
                if add_item == "on":
                    my_dict[f_key].update({'one_selection':True})
            elif key_parts[-1] == 'allow':
                if add_item == "on":
                    my_dict[f_key].update({'allow':True})
            elif key_parts[-1] == 'required':
                if add_item == "on":
                    my_dict[f_key].update({'required':True})
    # ######## returns an error if the image does not meet the standards
    if 'message' in check_image_upload_errors(request, form_pk, my_dict).keys():
        return check_image_upload_errors(request, form_pk, my_dict)['message']
    else:
        image_upload(request, pk, form_pk, my_dict)
    # ####### check None keys. If none, deletes that key
    for check_key, check_value in my_dict.items():
        for value_none in check_value.copy():
            if not check_value[value_none]:
                check_value.pop(value_none)
    # # for k,i in my_dict.items():
    #     # print(f"key>> {k} | value>> {i}")
    # print("my_dict>>>>", my_dict)
    return my_dict


