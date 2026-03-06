from flask import Flask, request, make_response, render_template, jsonify, abort
from flask_talisman import Talisman # pip install flask-talisman
import jwt
import json

app = Flask(__name__)
# In production, use environment variables for keys!
app.config['SECRET_KEY'] = "REALLY_LONG_COMPLEX_RANDOM_STRING_9988"

# Security Headers (CSP, HSTS, X-Frame-Options)
Talisman(app, content_security_policy=None) # CSP can be customized here

# Load secrets from the JSON "Database"
def load_db():
    with open('../db.json') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

def get_current_user():
    token = request.cookies.get('auth_token')
    if not token: return None
    try:
        # FIX 1: Strict algorithm enforcement and signature verification
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
        return None

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    token = jwt.encode({"user": username, "role": "guest"}, app.config['SECRET_KEY'], algorithm="HS256")
    
    resp = make_response(render_template('dashboard.html', user=username))
    # FIX 2: Secure Cookie Flags
    resp.set_cookie('auth_token', token, httponly=True, secure=False, samesite='Lax') 
    return resp

@app.route('/api/vault/<item_id>')
def get_vault(item_id):
    user_data = get_current_user()
    if not user_data: abort(401)
    
    db = load_db()
    item = db.get(item_id)
    # FIX 3: Authorization Check (Solving IDOR)
    if item and item['owner'] == user_data['user']:
        return jsonify(item)
    return jsonify({"error": "Unauthorized"}), 403

@app.route('/admin')
def admin_panel():
    user_data = get_current_user() # This helper now verifies the HS256 signature!
    
    if not user_data:
        return "Unauthorized: No valid token provided.", 401
    
    # Check if the role in the verified token is actually 'admin'
    if user_data.get('role') == 'admin':
        db = load_db()
        return render_template('admin.html', secret=db["2"]["secret"])
    
    # If a 'guest' tries to access this, they get a 403, even with a valid signature.
    return "Access Denied: You do not have Administrative privileges.", 403

@app.route('/logout')
def logout():
    resp = make_response("<h3>Logged out successfully!</h3><a href='/'>Go Home</a>")
    # This 'deletes' the cookie by setting its expiration to the past
    resp.set_cookie('auth_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Running on different port