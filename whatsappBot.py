import time
from flask import Flask, request, url_for, send_from_directory, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client  # Make sure to import the Twilio client
from parseYoutubeVideoUtils import fetch_transcript
from llamaAPITest import *
from sdTest import genImage
import json
import re
import os
import logging
import requests

app = Flask(__name__)

# Set up logging
# logging.basicConfig(level=logging.DEBUG)

def video_twitter_posts_old(transcript):
    posts = fetch_posts_from_video_old(transcript)
    logging.debug(f"Fetched posts: {posts}")
    posts_json = json.loads(posts)
    logging.debug(f"Posts JSON: {posts_json}")

    effect = posts_json.get('imageEffect', '')
    genre = posts_json.get('Genre', '')
    responses = []

    for i, p in enumerate(posts_json['posts']):
        if 'post' in p and 'prompt' in p:
            post = p['post']
            prompt = f"{p['prompt']},{effect},{genre}"
            image_url = f"http://localhost:5000/generate_image?prompt={prompt}&index={i}"
            response = requests.get(image_url)
            if response.status_code == 200:
                img_path = response.text
                img_url = url_for('serve_file', filename=os.path.basename(img_path), _external=True)
                responses.append((post, img_url))
                logging.debug(f"Generated image path: {img_path}")
            else:
                logging.error(f"Failed to generate image: {response.text}")
                responses.append((post, None))
        else:
            responses.append((p.get('post', ''), None))
    return responses
def video_instructional(transcript):
    posts = fetch_posts_from_video_instructional(transcript)
    logging.debug(f"Fetched posts: {posts}")
    posts_json = json.loads(posts)
    logging.debug(f"Posts JSON: {posts_json}")
    responses = []
    if 'post' in posts_json and 'prompt' in posts_json:
        post = posts_json['post']
        prompt = f"{posts_json['prompt']}"
        image_url = f"http://localhost:5000/generate_image?prompt={prompt}&index={0}"
        response = requests.get(image_url)
        if response.status_code == 200:
            img_path = response.text
            img_url = url_for('serve_file', filename=os.path.basename(img_path), _external=True)
            responses.append((post, img_url))
            logging.debug(f"Generated image path: {img_path}")
        else:
            logging.error(f"Failed to generate image: {response.text}")
            responses.append((post, None))
    else:
        responses.append((posts_json.get('post', ''), None))
    return responses
def video_general(transcript):
    outputs = fetch_posts_from_video_general(transcript)
    responses = []
    for i , posts in enumerate(outputs):
        logging.debug(f"Fetched posts: {posts}")
        posts_json = json.loads(posts)
        logging.debug(f"Posts JSON: {posts_json}")
        if 'post' in posts_json and 'prompt' in posts_json:
            post = posts_json['post']
            prompt = f"{posts_json['prompt']}"
            image_url = f"http://localhost:5000/generate_image?prompt={prompt}&index={i}"
            response = requests.get(image_url)
            if response.status_code == 200:
                img_path = response.text
                img_url = url_for('serve_file', filename=os.path.basename(img_path), _external=True)
                responses.append((post, img_url))
                logging.debug(f"Generated image path: {img_path}")
            else:
                logging.error(f"Failed to generate image: {response.text}")
                responses.append((post, None))
        else:
            responses.append((posts_json.get('post', ''), None))
    return responses

def video_twitter_posts(transcript):
    outputs = fetch_posts_from_video(transcript)
    responses = []
    k = 0
    for i , posts in enumerate(outputs):
        # print(posts)
        logging.debug(f"Fetched posts: {posts}")
        posts_json = json.loads(posts)
        print(posts_json)
        logging.debug(f"Posts JSON: {posts_json}")
        effect = posts_json.get('imageEffect', '')
        genre = posts_json.get('Genre', '')
        for j, p in enumerate(posts_json['posts']):
            if 'post' in p and 'prompt' in p:
                post = p['post']
                prompt = f"{p['prompt']},{effect},{genre}"
                image_url = f"http://localhost:5000/generate_image?prompt={prompt}&index={k}"
                response = requests.get(image_url)
                k = k + 1
                if response.status_code == 200:
                    img_path = response.text
                    img_url = url_for('serve_file', filename=os.path.basename(img_path), _external=True)
                    responses.append((post, img_url))
                    logging.debug(f"Generated image path: {img_path}")
                else:
                    logging.error(f"Failed to generate image: {response.text}")
                    responses.append((post, None))
            else:
                responses.append((p.get('post', ''), None))
    return responses
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

@app.route('/send_messages', methods=['POST'])
def send_messages():
    try:
        data = request.get_json()
        responses = data.get('responses', [])
        phone_number = data.get('phone_number')

        # Create a Twilio response object
        twilio_client = Client('ACc48856dd21f517da0937c40428a81753', 'ce102fd5e9005deaa695b875ac64c90d')

        for post, img_url in responses:
            message = twilio_client.messages.create(
                body=post,
                from_='whatsapp:+14155238886',
                to=f'whatsapp:{phone_number}',
                media_url=[img_url] if img_url else None
            )
            time.sleep(1)  # Ensures a delay between each message

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logging.error(f"Error sending messages: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        phone_number = request.values.get("From", "").replace("whatsapp:", "")
        logging.debug(f"Incoming message: {incoming_msg}, From: {phone_number}")

        youtube_pattern = r"(?:(?:https?:)?\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(youtube_pattern, incoming_msg)
        if match:
            video_id = match.group(1)
            logging.debug(f"YouTube video ID: {video_id}")
            transcript = fetch_transcript(video_id)
            responses = video_twitter_posts(transcript)
            send_message_data = {
                "responses": responses,
                "phone_number": phone_number
            }
            requests.post("http://localhost:5000/send_messages", json=send_message_data)
            return str(MessagingResponse().message("Your request is being processed. You will receive the results shortly."))

        else:
            return str(MessagingResponse().message("The provided input doesn't seem to be a valid YouTube link."))

    except Exception as e:
        logging.error(f"Error: {e}")
        return str(MessagingResponse().message(f"An error occurred: {e}")), 500

if __name__ == "__main__":
    if not os.path.exists('./out'):
        os.makedirs('./out')
    app.run(debug=True)
