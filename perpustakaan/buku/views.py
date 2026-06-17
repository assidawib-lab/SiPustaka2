from django.shortcuts import render
from django.db import connection

def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'")
        sedang_dipinjam = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dikembalikan'")
        sudah_dikembalikan = cursor.fetchone()[0] or 0

    context = {
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
    }
    return render(request, 'dashboard.html', context)