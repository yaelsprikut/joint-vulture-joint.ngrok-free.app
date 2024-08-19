import os
import re
import time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from pytube import YouTube
from pydub import AudioSegment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory where files are stored
UPLOAD_FOLDER = 'static'  # Change this to the directory where your files are stored
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html', time=time)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    
@app.route('/run-script', methods=['POST'])
def run_script():
    if request.method == 'POST':
        ytlink = request.form.get('ytlink')
        # Call your Python script or function here
        result = run_my_python_script(ytlink)
        return redirect(url_for('index'))

# Function to download the video and convert it to MP3
def download_youtube_to_mp3(youtube_url, output_path='.'):
    try:    
        # Download the highest resolution audio
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(only_audio=True).first()
        downloaded_file = video_stream.download(output_path=output_path)

        # Convert the downloaded file to MP3
        mp3_file = os.path.splitext(downloaded_file)[0] + '.mp3'
        audio = AudioSegment.from_file(downloaded_file)
        audio.export(mp3_file, format='mp3')

        # Optional: remove the original downloaded file
        os.remove(downloaded_file)

        filename = os.path.basename(mp3_file)
        return filename
    except Exception as e:
        print(e)
        return "Error: Please use a valid Youtube Video URL"
def run_my_python_script(youtube_url):
    # Your Python script logic here
    # Example usage
    output_path = "static"
    mp3_file_path = download_youtube_to_mp3(youtube_url, output_path)

    print('mp3_file_path: ', mp3_file_path)

    print(f'MP3 file saved at: {mp3_file_path}')
    print("Python script executed!")
    # filename = os.path.basename(mp3_file_path)
    if mp3_file_path == "Error: Please use a valid Youtube Video URL":
        flash(mp3_file_path, 'error')
    else: 
        flash(mp3_file_path, 'success')
    # You can return any result you want to display on the page
    # return "Script executed!"


if __name__ == '__main__':
    app.run(debug=True)
