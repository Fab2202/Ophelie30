import os
#from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import Flask, render_template, request, send_file, redirect, url_for, flash

import io
import zipfile
import os
_DEBUG = False
if not _DEBUG:
    import psycopg2

app = Flask(__name__)
#for dev:
app.secret_key = 'my_dev_secret_key_2710'

PHOTOS_FOLDER = os.path.join(app.static_folder, 'images')

secret_key = os.urandom(24)  # generates 24 random bytes

@app.route('/')
def index():
    
    return render_template('index.html')

if not _DEBUG:

    # Connexion à la base PostgreSQL (Scalingo met DATABASE_URL dans l'environnement)
    DATABASE_URL = os.environ.get('DATABASE_URL')

    def get_db_connection():
        conn = psycopg2.connect(DATABASE_URL)
        return conn

    # Créer la table si nécessaire
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS guestbook(
                id SERIAL PRIMARY KEY,
                author VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        conn.commit()
        cur.close()
        conn.close()

    create_table()

    @app.route('/livre_or', methods=['GET', 'POST'])
    def livre_or():
        if request.method == 'POST':
            author = request.form.get('author', '').strip()
            message = request.form.get('message', '').strip()

            if author and message:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('INSERT INTO guestbook (author, message) VALUES (%s, %s)', (author, message))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('livre_or'))

        conn = get_db_connection()
        cur = conn.cursor()
        # FRR-1010/2026: cur.execute('SELECT author, message, created_at FROM guestbook ORDER BY created_at DESC')
        cur.execute('SELECT id, author, message, created_at FROM guestbook ORDER BY created_at DESC')
        entries = cur.fetchall()
        cur.close()
        conn.close()

        return render_template('livre_or.html', entries=entries)


else:

    @app.route('/livre_or')
    def livre_or():
        #return 'under construction'
        #return render_template('contact.html')
        return render_template('livre_or.html')

@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM guestbook WHERE id = %s', (message_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('livre_or'))

@app.route('/photos')
def photos():
    # This page just lets users pick 2025 or 2026 galleries
    return render_template('photos.html')

def get_photo_filenames(folder):
    # List image files only
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
    try:
        files = os.listdir(os.path.join(app.static_folder, 'images', folder))
        photos = [f for f in files if os.path.splitext(f)[1].lower() in allowed_extensions]
        return photos
    except FileNotFoundError:
        return []

@app.route('/photos1996_1999')
def photos1996_1999():
    # Presumed you have a way to get photo filenames - example:
    photo_filenames = os.listdir(os.path.join(app.static_folder, 'images', 'photos1996_1999'))  # filter images if needed
    photos = [{'filename': fname, 'alt': fname} for fname in photo_filenames]
    return render_template('photos1996_1999.html', photos=photos)

@app.route('/photos1996_1999/<filename>')
def photo1996_1999_detail(filename):
    photos = get_photo_filenames('photos1996_1999')
    if filename not in photos:
        abort(404)
    img_url = url_for('static', filename=f'images/photos1996_1999/{filename}')
    return render_template('photo_detail.html', img_url=img_url, back_url=url_for('photos1996_1999'))

@app.route('/photos2000_2005')
def photos2000_2005():
    # Presumed you have a way to get photo filenames - example:
    photo_filenames = os.listdir(os.path.join(app.static_folder, 'images', 'photos2000_2005'))  # filter images if needed
    photos = [{'filename': fname, 'alt': fname} for fname in photo_filenames]
    return render_template('photos2000_2005.html', photos=photos)

@app.route('/photos2000_2005/<filename>')
def photo2000_2005_detail(filename):
    photos = get_photo_filenames('photos2000_2005')
    if filename not in photos:
        abort(404)
    img_url = url_for('static', filename=f'images/photos2000_2005/{filename}')
    return render_template('photo_detail.html', img_url=img_url, back_url=url_for('photos2000_2005'))

@app.route('/photos2006_2011')
def photos2006_2011():
    # Presumed you have a way to get photo filenames - example:
    photo_filenames = os.listdir(os.path.join(app.static_folder, 'images', 'photos2006_2011'))  # filter images if needed
    photos = [{'filename': fname, 'alt': fname} for fname in photo_filenames]
    return render_template('photos2006_2011.html', photos=photos)

@app.route('/photos2006_2011/<filename>')
def photo2006_2011_detail(filename):
    photos = get_photo_filenames('photos2006_2011')
    if filename not in photos:
        abort(404)
    img_url = url_for('static', filename=f'images/photos2006_2011/{filename}')
    return render_template('photo_detail.html', img_url=img_url, back_url=url_for('photos2006_2011'))

@app.route('/photos2012_2017')
def photos2012_2017():
    # Presumed you have a way to get photo filenames - example:
    photo_filenames = os.listdir(os.path.join(app.static_folder, 'images', 'photos2012_2017'))  # filter images if needed
    photos = [{'filename': fname, 'alt': fname} for fname in photo_filenames]
    return render_template('photos2012_2017.html', photos=photos)

@app.route('/photos2012_2017/<filename>')
def photo2012_2017_detail(filename):
    photos = get_photo_filenames('photos2012_2017')
    if filename not in photos:
        abort(404)
    img_url = url_for('static', filename=f'images/photos2012_2017/{filename}')
    return render_template('photo_detail.html', img_url=img_url, back_url=url_for('photos2012_2017'))

@app.route('/photos2018_2022')
def photos2018_2022():
    # Presumed you have a way to get photo filenames - example:
    photo_filenames = os.listdir(os.path.join(app.static_folder, 'images', 'photos2018_2022'))  # filter images if needed
    photos = [{'filename': fname, 'alt': fname} for fname in photo_filenames]
    return render_template('photos2018_2022.html', photos=photos)

@app.route('/photos2018_2022/<filename>')
def photo2018_2022_detail(filename):
    photos = get_photo_filenames('photos2018_2022')
    if filename not in photos:
        abort(404)
    img_url = url_for('static', filename=f'images/photos2018_2022/{filename}')
    return render_template('photo_detail.html', img_url=img_url, back_url=url_for('photos2018_2022'))

@app.route('/photos2023_2026')
def photos2023_2026():
    # Presumed you have a way to get photo filenames - example:
    photo_filenames = os.listdir(os.path.join(app.static_folder, 'images', 'photos2023_2026'))  # filter images if needed
    photos = [{'filename': fname, 'alt': fname} for fname in photo_filenames]
    return render_template('photos2023_2026.html', photos=photos)

@app.route('/photos2023_2026/<filename>')
def photo2023_2026_detail(filename):
    photos = get_photo_filenames('photos2023_2026')
    if filename not in photos:
        abort(404)
    img_url = url_for('static', filename=f'images/photos2023_2026/{filename}')
    return render_template('photo_detail.html', img_url=img_url, back_url=url_for('photos2023_2026'))

@app.route('/download_photos', methods=['POST'])
def download_photos():
    selected_photos = request.form.getlist('selected_photos')
    print("Selected photos:", selected_photos)
    if not selected_photos:
        flash('No photos selected for download.', 'warning')
        return redirect(url_for('photos1996_1999'))

    # Create in-memory ZIP file
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for fname in selected_photos:
            # Validate the file exists and prevent path traversal
            safe_fname = os.path.basename(fname)
            file_path = os.path.join(f'{PHOTOS_FOLDER}/photos1996_1999', safe_fname)
            if os.path.isfile(file_path):
                zf.write(file_path, arcname=safe_fname)
    memory_file.seek(0)

    # Send ZIP file for download
    return send_file(memory_file,
                     attachment_filename='photos_selected.zip',
                     as_attachment=True,
                     mimetype='application/zip')

from flask import request, send_file
import io
from zipfile import ZipFile
import os


if __name__ == '__main__':
    #lancement: flask run
    app.run(debug=True)