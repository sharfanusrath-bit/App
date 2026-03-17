from django.urls import path
from Users.views import *

urlpatterns = [
    path('userhome/', userhome, name='userhome'),
    path('upload_evidence/', upload_evidence, name='upload_evidence'),
    path('my_evidences/', my_evidences, name='my_evidences'),
]