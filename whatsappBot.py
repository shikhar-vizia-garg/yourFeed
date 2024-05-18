import time
from flask import Flask, request, send_file, url_for, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from parseYoutubeVideoUtils import fetch_transcript, get_video_id
from llamaAPITest import fetch_posts_from_video
from sdTest import genImage
import json
import re
import os
import logging
import requests

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/out/<path:filename>', methods=['GET'])
def serve_file(filename):
    try:
        return send_from_directory('out', filename)
    except Exception as e:
        logging.error(f"Error serving file {filename}: {e}")
        return "File not found", 404

@app.route('/generate_image', methods=['GET'])
def generate_image():
    prompt = request.args.get('prompt')
    index = request.args.get('index')
    if not prompt or not index:
        return "Missing 'prompt' or 'index' parameter", 400

    try:
        index = int(index)
    except ValueError:
        return "'index' parameter must be an integer", 400

    try:
        img_path = genImage(prompt, index)
        return img_path
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return "Error generating image", 500

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Get the incoming message
        incoming_msg = request.values.get("Body", "").strip()
        logging.debug(f"Incoming message: {incoming_msg}")

        # Create a Twilio response object
        resp = MessagingResponse()

        # Regular expression pattern to match YouTube video URLs
        youtube_pattern = r"(?:(?:https?:)?\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

        # Check if the incoming message is a YouTube link
        match = re.search(youtube_pattern, incoming_msg)
        if match:
            # Extract the video ID
            video_id = match.group(1)
            logging.debug(f"YouTube video ID: {video_id}")

            # Fetch the video transcript and perform further actions
            start_seconds = 0
            end_seconds = 900
            transcript = fetch_transcript(video_id, start_seconds, end_seconds)
            posts = fetch_posts_from_video(transcript)
            logging.debug(f"Fetched posts: {posts}")
            posts_json = json.loads(posts)
            logging.debug(f"Posts JSON: {posts_json}")

            effect = posts_json.get('imageEffect', '')
            genre = posts_json.get('Genre', '')
            image_paths = []

            for i, p in enumerate(posts_json['posts']):
                if 'post' in p and 'prompt' in p:
                    post = p['post']
                    prompt = f"{p['prompt']},{effect},{genre}"
                    image_url = f"http://localhost:5000/generate_image?prompt={prompt}&index={i}"
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        img_path = response.text
                        image_paths.append(img_path)
                        logging.debug(f"Generated image path: {img_path}")
                    else:
                        logging.error(f"Failed to generate image: {response.text}")
                        image_paths.append(None)

            for i, p in enumerate(posts_json['posts']):
                if 'post' in p:
                    if image_paths[i]:
                        image_url = url_for('serve_file', filename=os.path.basename(image_paths[i]), _external=True)
                        resp.message(p['post']).media(image_url)
                    else:
                        resp.message(p['post']).media("Image generation failed")
        else:
            resp.message("The provided input doesn't seem to be a valid YouTube link.")

        return str(resp)

    except Exception as e:
        logging.error(f"Error: {e}")
        return str(MessagingResponse().message(f"An error occurred: {e}")), 500

if __name__ == "__main__":
    # Ensure the output directory exists
    if not os.path.exists('./out'):
        os.makedirs('./out')
    app.run(debug=True)
