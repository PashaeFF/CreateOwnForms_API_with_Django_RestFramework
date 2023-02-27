from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>', views.create_values_for_form),
    path('<int:pk>/view', views.get_form),
    # path('<int:pk>/list', views.get_the_list_of_filled_form),
    # path('<int:pk>/download', views.form_id_to_xlsx),
    # path('<int:pk>/delete_filled_form', views.delete_filled_form),
    # path('<int:pk>/view_filled_form/<int:wk>', views.delete_filled_form),
    # path('<int:pk>/delete', views.delete_form),
    # path('<int:pk>/filled_form/<int:wk>/view', views.get_filled_form),
    # path('<int:pk>/filled_form/<int:wk>/download', views.filled_form_to_xlsx),
]