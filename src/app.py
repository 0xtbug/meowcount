from flask import Flask, render_template, request, redirect, jsonify, session, url_for, send_file
from dotenv import load_dotenv
import requests, os, urllib.parse, logging

load_dotenv()

# Config
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

# App setup
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = True

logging.basicConfig(level=logging.INFO)

# Utilities
def get_token(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI + '/auth',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        logging.error(f"Token exchange failed: {e} - {r.text}")
        raise

    return r.json()

def set_header(access_token, token_type):
    return {
        "Authorization": f"{token_type} {access_token}"
    }

def get_server_count(header):
    r = requests.get("https://discord.com/api/users/@me/guilds", headers=header)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        logging.error(f"Guild fetch failed: {e} - {r.text}")
        raise
    return len(r.json())

# Routes
@app.route('/')
def index():
    if 'access_token' in session:
        try:
            header = set_header(session['access_token'], session['token_type'])
            server_count = get_server_count(header)
            user_info = requests.get("https://discord.com/api/users/@me", headers=header)
            user_info.raise_for_status()

            return render_template(
                "index.html",
                authenticated=True,
                server_count=server_count,
                user=user_info.json().get('username', 'Unknown'),
                client_id=CLIENT_ID,
                redirect_url=urllib.parse.quote_plus(REDIRECT_URI + "/auth")
            )
        except Exception as e:
            logging.warning(f"Session error: {e}")
            session.clear()
            return redirect('/')

    return render_template(
        "index.html",
        page_title="MeowCount - Discord Server Counter",
        authenticated=False,
        client_id=CLIENT_ID,
        redirect_url=urllib.parse.quote_plus(REDIRECT_URI + "/auth")
    )

@app.route('/auth')
def auth():
    code = request.args.get('code')
    if not code:
        return "Missing code", 400

    try:
        token = get_token(code)
        session['access_token'] = token['access_token']
        session['token_type'] = token['token_type']
    except Exception as e:
        logging.error(f"Auth error: {e}")
        return "Authentication failed", 500

    return redirect('/')

@app.route('/api/refresh', methods=['POST'])
def refresh():
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        header = set_header(session['access_token'], session['token_type'])
        server_count = get_server_count(header)
        user_info = requests.get("https://discord.com/api/users/@me", headers=header)
        user_info.raise_for_status()

        return jsonify({
            'server_count': server_count,
            'username': user_info.json().get('username', 'Unknown')
        })
    except Exception as e:
        logging.error(f"Refresh error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/robots.txt')
def robots():
    return send_file("robots.txt")
