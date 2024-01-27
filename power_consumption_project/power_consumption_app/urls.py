from django.urls import path
from . import views

urlpatterns = [
   # path('', views.get_power_data, name='get_power_data'),
    path('latest_data/',views.latest_data,name = 'latest_data'),
    path('latest_voltage_data/',views.latest_voltage_data,name = 'latest_voltage_data'),
    path('latest_electrictiy_data/',views.latest_electrictiy_data,name = 'latest_electrictiy_data'),
    path('current/',views.current, name = 'current'),
    path('voltage/',views.voltage,name = 'voltage'),
    path('elec_con/',views.elec_con,name = 'elec_con'),
    
]
