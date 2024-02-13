
import sqlite3
from flask import Flask, render_template, request, session, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# fungsi untuk cek anemia atau tidak berdasarkan hb dari jenis kelamin
def is_anemic(hb, jk):
  if jk == "L":
    if float(hb) < 13.5:
        status= "ANEMIA"
    else:
        status ="TIDAK ANEMIA"
  elif jk == "P":
    if float(hb) < 12.0:
        status= "ANEMIA"
    else:
        status ="TIDAK ANEMIA"
  else:
    raise ValueError("Jenis kelamin tidak valid")
  
  return status

app = Flask(__name__)


# data admin login
users = {    'admin': 'admin',  }  


# route unutk akses halaman login
@app.route('/login', methods=['GET', 'POST'])  

# fungsi unutk melakukan login atau belum
def login():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
        if username in users and users[username] == password:  
            session['username'] = username  
            return redirect(url_for('index'))  
        else:  
            return render_template('login.html', error='Invalid username or password')  
    else:  
        return render_template('login.html')  



# route unutk akses halaman index
@app.route('/')
def index():
    # kondisi unutk cek login atau belum
    if 'username' in session:  
        conn = get_db_connection()
        pasiens = conn.execute('SELECT * FROM pasiens').fetchall()
        totalPasien = conn.execute('SELECT count(*) FROM pasiens').fetchone()[0]
        pasienAnemia = conn.execute('SELECT count(*) FROM pasiens WHERE status = ?',('ANEMIA',)).fetchone()[0]
        pasienTidakAnemia = conn.execute('SELECT count(*) FROM pasiens WHERE status = ?',('TIDAK ANEMIA',)).fetchone()[0]
      
        conn.close()
        return render_template('index.html', pasiens=pasiens,total=totalPasien,pasienAnemia=pasienAnemia,pasienTidakAnemia=pasienTidakAnemia)
    else:  
        return redirect(url_for('login'))  


# funsi unutk akses halaman tanbah data
@app.get('/create')
def create_get():
    return render_template('create.html')

# funsi unutk menerima data inpytan dan menyimpan data ke database
@app.post('/create')
def create_post():
    if request.method =='POST':
        nama_pasien=request.form.get('nama_pasien',type=str)
        jenis_kelamin= request.form.get('jenis_kelamin')
        hb= request.form.get('hb',type=float)
        mch= request.form.get('mch',type=float)
        mchc= request.form.get('mchc',type=float)
        mcv= request.form.get('mcv',type=float)
        if  not hb or not mch or not mchc or not mcv or not jenis_kelamin:
         flash('data gagal di input ')  
        else:
            status= is_anemic(hb,jenis_kelamin)

            conn = get_db_connection()
            conn.execute('INSERT INTO pasiens (nama_pasien,jenis_kelamin,hb,mch,mchc,mcv,status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (nama_pasien, jenis_kelamin,hb,mch,mchc,mcv,status))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


# fungsi unutk keluar
@app.route('/keluar')  
def logout():  
    session.pop('username', None)  
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
