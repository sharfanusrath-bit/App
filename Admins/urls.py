from django.urls import path
from Admins.views import *

urlpatterns = [
    path('adminhome/', adminhome, name='adminhome'),
    path('admin_update_userstatus/<int:user_id>/', admin_update_userstatus, name='admin_update_userstatus'),
    path('admin_all_evidence/', admin_all_evidence, name='admin_all_evidence'),
    path('admin/evidence/update/<int:evidence_id>/', update_evidence_status, name='update_evidence_status'),
    path('verify_transaction', verify_transaction, name='verify_transaction'),

]