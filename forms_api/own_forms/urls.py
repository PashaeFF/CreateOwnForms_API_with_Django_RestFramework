from django.urls import path
from .views import FormsView

urlpatterns = [
    path('', FormsView.index),
    path('<int:pk>', FormsView.create_values_for_form),
    path('<int:pk>/view', FormsView.get_form),
    path('<int:pk>/list/', FormsView.get_the_list_of_filled_form),
    # path('<int:pk>/download', FormsView.form_id_to_xlsx),
    # path('<int:pk>/delete_filled_form', FormsView.delete_filled_form),
    # path('<int:pk>/view_filled_form/<int:wk>', FormsView.delete_filled_form),
    # path('<int:pk>/delete', FormsView.delete_form),
    path('<int:pk>/filled_form/<int:wk>/view', FormsView.get_filled_form),
    # path('<int:pk>/filled_form/<int:wk>/download', FormsView.filled_form_to_xlsx),
]