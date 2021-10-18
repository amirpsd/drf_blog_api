from django.urls import path, include

app_name = 'category'


urlpatterns = [
    path('api/', include('blog_category.api.urls'))
]   
