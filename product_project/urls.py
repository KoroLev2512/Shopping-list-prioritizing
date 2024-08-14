from django.urls import path, re_path, include
from add_product import views

product_patterns = [
    path('<str:name>/', views.user, name='user'),
    path('add_user', views.add_user, name='add_user'),
    path('delete_user', views.delete_user, name='delete_user')
    # re_path(r'^(family|семья)/$', views.family2, kwargs={"name":"family"}, name='fam'), # Через регулярку
]

voting_patterns = [
    # path('', views.voting),  # Маршрут по умолчанию
    path('<str:name>', views.voting, name='golos'),  # Через парметры маршрута
]

urlpatterns = [
    path('', views.home, name='home'), # Главная страница
    path('result', views.result, name='result'), # Результат матрицы
    path("products/", include(product_patterns)), # Все связанное с заполнением товара
    path("voting/", include(voting_patterns)), # Все связанное с голосованием
]
