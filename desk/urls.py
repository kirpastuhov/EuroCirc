from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.views import LoginView
from desk.views import Index, CreateCity, Days, CreateDay, Odeum, Box, Stats, CityStats


app_name = 'desk'


urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('create_city/', CreateCity.as_view(), name='create_city'),
	path('days/<int:city_id>', Days.as_view(), name='days'),
	path('create_day/<int:city_id>', CreateDay.as_view(), name='create_day'),
	path('odeum/<str:date>/<str:hour>/<int:city_id>', Odeum.as_view(), name='odeum'),
	path('box/<str:sector_number>/<str:date>/<str:hour>/<int:city_id>', Box.as_view(), name='box'),
	path('city_stats/<int:city_id>', CityStats.as_view(), name='city_stats'),
	path('stats/<str:date>/<str:hour>/<int:city_id>', Stats.as_view(), name='stats'),
	path('login/', LoginView.as_view(), name='login')
]
