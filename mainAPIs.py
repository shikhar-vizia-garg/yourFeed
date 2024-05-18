from flask import Flask, jsonify, render_template
from parseYoutubeVideoUtils import fetch_transcript
from llamaAPITest import fetch_posts_from_video
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_posts_from_video', methods=['POST'])
def fetch_posts_from_video_api():
    video_id = "pTTkM-NHylw"
    start_seconds = 0
    end_seconds = 900
    transcript = fetch_transcript(video_id, start_seconds, end_seconds)
    posts = fetch_posts_from_video(transcript)
    posts_json = json.loads(posts)
    print(posts_json)
    out = jsonify(posts)
    print(out)
    return out

if __name__ == '__main__':
    app.run(debug=True)
