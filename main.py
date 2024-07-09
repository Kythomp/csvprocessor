from flask import Flask, request, render_template, redirect, url_for
import os
import csv
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    team_column_name = request.form['team_column']
    photo_column_name = request.form['photo_column']
    custom_folder_name = request.form['custom_folder']

    csv_file = request.files['csv_file']
    folder_files = request.files.getlist('folder')
    destination_folder_path = request.form['destination_folder']

    # Create the custom folder inside the destination folder
    sorted_photos_folder = os.path.join(destination_folder_path, custom_folder_name)
    if not os.path.exists(sorted_photos_folder):
        os.makedirs(sorted_photos_folder)
        print(f"Created folder: {sorted_photos_folder}")

    unlisted_folder = os.path.join(sorted_photos_folder, "Unsorted")
    if not os.path.exists(unlisted_folder):
        os.makedirs(unlisted_folder)
        print(f"Created unlisted folder: {unlisted_folder}")

    listed_photos = set()

    # Process the CSV file
    csv_content = csv_file.read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(csv_content)

    for row in csv_reader:
        team_name = row.get(team_column_name, "").strip()
        photo_name = row.get(photo_column_name, "").strip()

        if team_name and photo_name:
            for folder_file in folder_files:
                if folder_file.filename == photo_name:
                    listed_photos.add(photo_name)
                    team_folder = os.path.join(sorted_photos_folder, team_name)
                    if not os.path.exists(team_folder):
                        os.makedirs(team_folder)
                    folder_file.save(os.path.join(team_folder, photo_name))

    # Move unlisted photos
    for folder_file in folder_files:
        if folder_file.filename not in listed_photos:
            folder_file.save(os.path.join(unlisted_folder, folder_file.filename))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
