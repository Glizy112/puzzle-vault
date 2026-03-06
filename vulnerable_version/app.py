from flask import Flask, request, make_response, render_template, jsonify
from datetime import datetime
import jwt # PyJWT
import json

app = Flask(__name__)

# Load from the JSON file
def load_db():
    with open('../db.json') as f:
        return json.load(f)

#Home route
@app.route('/')
def index():
    return render_template('index.html')

#Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    db = load_db()
    # THE INSPECTOR KEY: Hidden inside the JWT Payload
    # Hint: You can find this by pasting your token into jwt.io
    payload = {
        "user": username, 
        "role": "guest" 
    }
    payload["hint"] = db["hint"]
    
    # VULNERABILITY 1: Insecure JWT creation
    token = jwt.encode(payload, db["key"], algorithm="HS256")
    
    resp = make_response(render_template('dashboard.html', user=username))
    
    # VULNERABILITY 2: Insecure Cookie Flags (Missing HttpOnly, Secure)
    resp.set_cookie('auth_token', token) 
    
    # THE HIDDEN RECON HEADER
    # This is a common "Developer Oversight" in real apps
    resp.headers['X-Debug-Mode'] = "Enabled"
    resp.headers['X-Internal-Route'] = "/internal/system_status"
    
    return resp

#Another Route
@app.route('/internal/system_status')
def internal_status():
    db = load_db()
    # This route leaks server information!
    server_info = db["ser_inf"]
    server_info["app_secret_key"] = db["key"]

    #calculating server date and time
    now = datetime.now()
    time_format = now.strftime("%B %d, %Y %H:%M:%S")

    server_info["server_time"] = time_format
    return jsonify(server_info)

#Yet Another Route
@app.route('/api/vault/<item_id>')
def get_vault(item_id):
    # VULNERABILITY 3: IDOR - No check if current user owns this ID
    db = load_db()
    item = db.get(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

#Protected Route
@app.route('/admin')
def admin_panel():
    token = request.cookies.get('auth_token')
    if not token: return "No token found", 401
    # VULNERABILITY 4: JWT None Algorithm Exploit
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    if decoded.get('role') == 'admin':
        db = load_db()
        return render_template('admin.html', secret=db["2"]["secret"])
    return "Access Denied! Only admins allowed.", 403

#Logout Route
@app.route('/logout')
def logout():
    resp = make_response("<h3>Logged out successfully!</h3><a href='/'>Go Home</a>")
    # After logout, delete the cookie by setting its expiration to the past
    resp.set_cookie('auth_token', '', expires=0)
    return resp

#Main driver function
if __name__ == '__main__':
    app.run(debug=True, port=5000)