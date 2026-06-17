from django.shortcuts import render, redirect
from django.db import connection

def list_siswa(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa ORDER BY id ASC")
        columns = [col[0] for col in cursor.description]
        data_siswa = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'siswa/list_siswa.html', {'data_siswa': data_siswa})

def tambah_siswa(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        nis = request.POST.get('nis')
        is_active = True if request.POST.get('is_active') == 'on' else False

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO siswa (nama, kelas, nis, is_active)
                VALUES (%s, %s, %s, %s)
            """, [nama, kelas, nis, is_active])
        return redirect('list_siswa')
    return render(request, 'siswa/tambah_siswa.html')

def edit_siswa(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            nama = request.POST.get('nama')
            kelas = request.POST.get('kelas')
            nis = request.POST.get('nis')
            is_active = True if request.POST.get('is_active') == 'on' else False

            cursor.execute("""
                UPDATE siswa SET nama=%s, kelas=%s, nis=%s, is_active=%s WHERE id=%s
            """, [nama, kelas, nis, is_active, id])
            return redirect('list_siswa')

        cursor.execute("SELECT * FROM siswa WHERE id = %s", [id])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        siswa = dict(zip(columns, row))

    return render(request, 'siswa/edit_siswa.html', {'siswa': siswa})

def detail_siswa(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa WHERE id = %s", [id])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        siswa = dict(zip(columns, row))
    return render(request, 'siswa/detail_siswa.html', {'siswa': siswa})

def hapus_siswa(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM siswa WHERE id = %s", [id])
    return redirect('list_siswa')