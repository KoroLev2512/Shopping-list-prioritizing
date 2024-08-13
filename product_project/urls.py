from django.urls import path, re_path, include
from add_product import views

product_patterns = [
    path('mother', views.mother, kwargs={"name":"mother"}, name='mother'),
    path('father', views.father, kwargs={"name":"father"}, name='father'),
    path('son', views.son, kwargs={"name":"son"}, name='son'),
    path('family', views.family, kwargs={"name":"family"}, name='family'),
    # re_path(r'^(family|семья)/$', views.family2, kwargs={"name":"family"}, name='fam'), # Через регулярку
]

voting_patterns = [
    # path('', views.voting),  # Маршрут по умолчанию
    path('<str:name>', views.voting, name='golos'),  # Через парметры маршрута
]

urlpatterns = [
    path('', views.index, name='Home'), # Главная страница
    path('result', views.result, name='Result'), # Главная страница
    path("products/", include(product_patterns)), # Все связанное с заполнением товара
    path("voting/", include(voting_patterns)), # Все связанное с голосованием
]
