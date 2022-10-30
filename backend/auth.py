from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from database.db import db, get_all_collection, storage
from firebase_admin import firestore
from functools import wraps

auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('auth.login'))
    return wrapper

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # tangkap datanyas
        data = {
            'username' : request.form['username'],
            'password': request.form['password']
        }
        # cek data di database
        users_ref = db.collection('users').where('username', '==', data['username']).stream()
        user = {}
        for use in users_ref:
            user = use.to_dict()
        
        if user:
            if check_password_hash(user['password'], data['password']):
                session['user'] = user
                flash('Berhasil Login', 'success')
                return redirect(url_for('mahasiswa'))
            else:
                flash('Password / Username Anda Salah', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Password / Username Salah', 'danger')
            return redirect(url_for('auth.login'))
            
    if 'user' in session:
        return redirect(url_for('mahasiswa'))
    return render_template('login.html')

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = {
            'created_at': firestore.SERVER_TIMESTAMP,
            'username': request.form['username'].lower()
        }
        
        password = request.form['password']
        password_1 = request.form['password_1']

        if password_1 != password:
            flash('Password Tidak Sama', 'danger')
            return redirect(url_for('auth.register'))
        
        users_ref = db.collection('users').where('username', '==', data['username']).stream()
        user = {}
        for use in users_ref:
            user = use.to_dict()
            
        if user:
            flash('Username Sudah Terdaftar', 'danger')
            return redirect(url_for('auth.register'))
        
        
        
        data['password'] = generate_password_hash(password, 'sha256')
        
        db.collection('users').document().set(data)
        flash('Pendaftaran Berhasil', 'success')
        return redirect(url_for('auth.login'))
        
        # return jsonify(data)
        
        
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

