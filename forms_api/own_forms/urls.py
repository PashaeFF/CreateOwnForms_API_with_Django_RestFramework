from django.urls import path
from .views import FormsAll, CreateForm, ViewForm

from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



urlpatterns = [
    path('', FormsAll.as_view()),
    path('form/', CreateForm.as_view()),
    path('<int:pk>', ViewForm.as_view()),
    # path('<int:pk>', CreateFormValues.as_view()),
    # path('<int:pk>/view', Forms.get_form),
    # path('<int:pk>/list/', Forms.get_the_list_of_filled_form),
    # # path('<int:pk>/download', FormsView.form_id_to_xlsx),
    # path('<int:pk>/delete_filled_form/<int:wk>', DeleteFilledForm.as_view()),
    # path('<int:pk>/delete', DeleteForm.as_view()),
    # path('<int:pk>/filled_form/<int:wk>/view', Forms.get_filled_form),
    # # path('<int:pk>/filled_form/<int:wk>/download', FormsView.filled_form_to_xlsx),
    
]