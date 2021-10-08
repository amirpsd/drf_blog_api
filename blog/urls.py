from django.urls import path, include

app_name = 'blog'


urlpatterns = [
    path('api/',include('blog.api.urls'))
]   
