from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomeView, PengamatanView, DetailPengamatanView

urlpatterns = [
  path('', HomeView.as_view(), name='biodiversity_home'),
  path('<int:page>/', PengamatanView.as_view(), name='biodiversity_pengamatan'),
  path('pengamatan/<int:page>/', DetailPengamatanView.as_view(), name='biodiversity_detail_pengamatan'),
]