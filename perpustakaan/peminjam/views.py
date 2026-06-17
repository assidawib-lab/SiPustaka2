from django.shortcuts import render, redirect
from django.db import connection

# ==========================================
# FUNGSI 1: MENAMPILKAN DAFTAR BUKU (R - Read)
# ==========================================
def list_buku(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku ORDER BY id ASC")
        columns = [col[0] for col in cursor.description]
        data_buku = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'data_buku': data_buku}
    return render(request, 'buku/list_buku.html', context)


# ==========================================
# FUNGSI 2: MENAMBAH BUKU BARU (C - Create)
# ==========================================
def tambah_buku(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        pengarang = request.POST.get('pengarang')
        kategori = request.POST.get('kategori')
        penerbit = request.POST.get('penerbit')
        tahun_terbit = request.POST.get('tahun_terbit')
        rak = request.POST.get('rak')
        stok = request.POST.get('stok')
        deskripsi = request.POST.get('deskripsi')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO buku (judul, pengarang, ketagori, penerbit, tahun_terbit, rak, stok, deskripsi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi])
        
        return redirect('list_buku')
    
    return render(request, 'buku/tambah_buku.html')


# ==========================================
# FUNGSI 3: MENGUBAH DATA BUKU (U - Update)
# ==========================================
def edit_buku(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            judul = request.POST.get('judul')
            pengarang = request.POST.get('pengarang')
            kategori = request.POST.get('kategori')
            penerbit = request.POST.get('penerbit')
            tahun_terbit = request.POST.get('tahun_terbit')
            rak = request.POST.get('rak')
            stok = request.POST.get('stok')
            deskripsi = request.POST.get('deskripsi')

            cursor.execute("""
                UPDATE buku 
                SET judul=%s, pengarang=%s, ketagori=%s, penerbit=%s, tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s
                WHERE id=%s
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi, id])
            
            return redirect('list_buku')

        # Ambil data lama untuk ditampilkan di form
        cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
        row = cursor.fetchone()
        
        columns = [col[0] for col in cursor.description]
        buku = dict(zip(columns, row))

    return render(request, 'buku/edit_buku.html', {'buku': buku})

def hapus_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE buku_id = %s AND status != 'Dikembalikan'", [id])
        active_count = cursor.fetchone()[0]

        if active_count > 0:
            return render(request, 'buku/hapus_buku_error.html', {
                'book_id': id,
                'active_count': active_count,
            })

        cursor.execute("DELETE FROM peminjaman WHERE buku_id = %s AND status = 'Dikembalikan'", [id])
        cursor.execute("DELETE FROM buku WHERE id = %s", [id])
    
    return redirect('list_buku')

def detail_buku(request, id):
    with connection.cursor() as cursor:
        # Ambil data 1 buku berdasarkan ID
        cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
        row = cursor.fetchone()
        
        # Ubah jadi dictionary
        columns = [col[0] for col in cursor.description]
        buku = dict(zip(columns, row))

    return render(request, 'buku/detail_buku.html', {'buku': buku})

def list_peminjaman(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama AS nama_siswa, b.judul AS judul_buku,
                   p.tanggal_pinjam, p.jatuh_tempo, p.status
            FROM peminjaman p
            JOIN siswa s ON p.siswa_id = s.id
            JOIN buku b ON p.buku_id = b.id
            ORDER BY p.id ASC
        """)
        columns = [col[0] for col in cursor.description]
        data_peminjaman = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'peminjam/list_peminjaman.html', {'data_peminjaman': data_peminjaman})


def tambah_peminjaman(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa WHERE is_active = TRUE ORDER BY nama ASC")
        columns_siswa = [col[0] for col in cursor.description]
        siswa_list = [dict(zip(columns_siswa, row)) for row in cursor.fetchall()]

        cursor.execute("SELECT * FROM buku WHERE stok > 0 ORDER BY judul ASC")
        columns_buku = [col[0] for col in cursor.description]
        buku_list = [dict(zip(columns_buku, row)) for row in cursor.fetchall()]

    if request.method == 'POST':
        siswa_id = request.POST.get('siswa_id')
        buku_id = request.POST.get('buku_id')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        jatuh_tempo = request.POST.get('jatuh_tempo')
        keperluan = request.POST.get('keperluan')
        status = request.POST.get('status')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status])

            if status == 'Dipinjam':
                cursor.execute("UPDATE buku SET stok = stok - 1 WHERE id = %s AND stok > 0", [buku_id])

        return redirect('list_peminjaman')

    return render(request, 'peminjam/tambah_peminjaman.html', {
        'siswa_list': siswa_list,
        'buku_list': buku_list,
    })


def ubah_status(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM peminjaman WHERE id = %s", [id])
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        peminjaman = dict(zip(columns, row))

    if request.method == 'POST':
        new_status = request.POST.get('status')
        old_status = peminjaman['status']
        buku_id = peminjaman['buku_id']

        with connection.cursor() as cursor:
            if old_status != new_status:
                if old_status != 'Dikembalikan' and new_status == 'Dikembalikan':
                    cursor.execute("UPDATE buku SET stok = stok + 1 WHERE id = %s", [buku_id])
                elif old_status == 'Dikembalikan' and new_status == 'Dipinjam':
                    cursor.execute("UPDATE buku SET stok = stok - 1 WHERE id = %s AND stok > 0", [buku_id])

            cursor.execute("UPDATE peminjaman SET status = %s WHERE id = %s", [new_status, id])

        return redirect('list_peminjaman')

    return render(request, 'peminjam/ubah_status.html', {'peminjaman': peminjaman})


def dashboard(request):
    with connection.cursor() as cursor:
        # Menghitung total stok buku keseluruhan
        cursor.execute("SELECT SUM(stok) FROM buku")
        total_buku = cursor.fetchone()[0] or 0

        # Menghitung total macam/judul buku
        cursor.execute("SELECT COUNT(*) FROM buku")
        total_judul = cursor.fetchone()[0] or 0