"""
URL configuration for perpustakaan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from siswa import views as siswa_views
from peminjam import views as peminjaman_views

urlpatterns = [
    path('', siswa_views.list_siswa, name='list_siswa'),
    path('siswa/', siswa_views.list_siswa, name='list_siswa'),
    path('siswa/tambah/', siswa_views.tambah_siswa, name='tambah_siswa'),
    path('siswa/edit/<int:id>/', siswa_views.edit_siswa, name='edit_siswa'),
    path('siswa/detail/<int:id>/', siswa_views.detail_siswa, name='detail_siswa'),
    path('siswa/hapus/<int:id>/', siswa_views.hapus_siswa, name='hapus_siswa'),
    path('buku/', peminjaman_views.list_buku, name='list_buku'),
    path('buku/tambah/', peminjaman_views.tambah_buku, name='tambah_buku'),
    path('buku/edit/<int:id>/', peminjaman_views.edit_buku, name='edit_buku'),
    path('buku/detail/<int:id>/', peminjaman_views.detail_buku, name='detail_buku'),
    path('buku/hapus/<int:id>/', peminjaman_views.hapus_buku, name='hapus_buku'),
    path('peminjaman/', peminjaman_views.list_peminjaman, name='list_peminjaman'),
    path('peminjaman/tambah/', peminjaman_views.tambah_peminjaman, name='tambah_peminjaman'),
    path('peminjaman/ubah-status/<int:id>/', peminjaman_views.ubah_status, name='ubah_status'),
]