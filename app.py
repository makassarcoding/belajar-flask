from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from database.db import db, get_all_collection, storage
from firebase_admin import firestore
from functools import wraps
from backend.auth import login_required, auth
# ===============================================

# Starter Template Flask
# By Makassar Coding

# ================================================
# Menentukan Nama Folder Penyimpanan Asset
app = Flask(__name__, static_folder='static', static_url_path='')
# Untuk Menggunakan flash pada flask
app.secret_key = 'iNiAdalahsecrEtKey'
# Untuk Mentukan Batas Waktu Session
app.permanent_session_lifetime = datetime.timedelta(days=7)
# Menentukan Jumlah Maksimal Upload File
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

app.register_blueprint(auth)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mahasiswa')
@login_required
def mahasiswa():  
    
    
    daftar_mahasiswa = get_all_collection('mahasiswa')
    
    return render_template('mahasiswa/mahasiswa.html',mahasiswa=daftar_mahasiswa)

@app.route('/mahasiswa/tambah', methods=['GET', 'POST'])
@login_required
def tambah_mahasiswa():
    if request.method == 'POST':
        # KITA TAMPUNG DULU DATANYA DI DICT
        data = {
            'created_at': firestore.SERVER_TIMESTAMP,
            'nama_lengkap' : request.form['nama_lengkap'],
            'nim' : request.form['nim'],
            'status' : request.form['status'],
            'jenis_kelamin' : request.form['jenis_kelamin'],
            'tgl_lahir' : request.form['tgl_lahir'],
            'jurusan' : request.form['jurusan'],
        }
        
        if 'image' in request.files and request.files['image']:
            image = request.files['image']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"mahasiswa/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['photoURL'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('mahasiswa'))
            
        # MASUKKAN DATA KE DATABASE
        db.collection('mahasiswa').document().set(data)
        # KEMBALI KE HALAMAN MAHASISWA
        flash('Berhasil menambahkan data', 'success')
        return redirect(url_for('mahasiswa'))
        # return jsonify()
        
    jurusan = get_all_collection('jurusan')
    return render_template('mahasiswa/tambah_mahasiswa.html', data=jurusan)

# READ
@app.route('/mahasiswa/<uid>')
@login_required
def lihat_mahasiswa(uid):
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('mahasiswa/lihat_mahasiswa.html', mahasiswa=mahasiswa)

# UPDATE
@app.route('/mahasiswa/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_mahasiswa(uid):
    if request.method == 'POST':
        # KITA TAMPUNG DULU DATANYA DI DICT
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'nim' : request.form['nim'],
            'status' : request.form['status'],
            'jenis_kelamin' : request.form['jenis_kelamin'],
            'tgl_lahir' : request.form['tgl_lahir'],
            'jurusan' : request.form['jurusan'],
        }
        # MASUKKAN DATA KE DATABASE
        db.collection('mahasiswa').document(uid).update(data)
        # KEMBALI KE HALAMAN MAHASISWA
        flash('Berhasil Mengedit data', 'success')
        return redirect(url_for('mahasiswa'))
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('mahasiswa/edit_mahasiswa.html', mahasiswa=mahasiswa)

# HAPUS
@app.route('/mahasiswa/hapus/<uid>')
@login_required
def hapus_mahasiswa(uid):
    db.collection('mahasiswa').document(uid).delete()
    flash('Berhasil Hapus Data', 'danger')
    return redirect(url_for('mahasiswa'))


# ================================================================================



#==============================================================================================
@app.route('/jurusan', methods=['POST', 'GET'])
def jurusan():
    if request.method == 'POST':
        data = {
            'created_at': firestore.SERVER_TIMESTAMP,
            'jurusan' : request.form['jurusan']
        }
        
        db.collection('jurusan').document().set(data)
        flash('Berhasil Menambahkan Jurusan', 'success')
        return redirect(url_for('jurusan'))
    
    daftar_jurusan = get_all_collection('jurusan')
    return render_template('jurusan/jurusan.html', data=daftar_jurusan)

@app.route('/jurusan/edit', methods=['POST'])
def edit_jurusan():
    if request.method == 'POST':
        uid = request.form['id_jurusan']
        data = {
            'jurusan' : request.form['nama_jurusan']
        }
        
        db.collection('jurusan').document(uid).update(data)
        flash('Berhasil Edit Jurusan', 'success')
        return redirect(url_for('jurusan'))



# Untuk Menjalankan Program Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)