from flask import Flask, request, send_file, jsonify
import pandas as pd
import os
import io
from datetime import datetime

app = Flask(__name__)
LOG_FILE = 'sent_log.csv'

@app.route('/track')
def track():
    email = request.args.get('email')
    tracking_id = request.args.get('id')
    
    print(f"Tracking request: email={email}, tracking_id={tracking_id}")
    
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            
            if tracking_id:
                mask = (df['Tracking ID'] == tracking_id) & (df['Status'] == 'not viewed')
            else:
                mask = (df['Receiver Email'] == email) & (df['Status'] == 'not viewed')
            
            if mask.any():
                df.loc[mask, 'Status'] = 'viewed'
                df.to_csv(LOG_FILE, index=False)
                print(f"Updated status to 'viewed' for tracking_id: {tracking_id}")
            else:
                print(f"No matching entry found for tracking_id: {tracking_id}")
                
        except Exception as e:
            print(f"Error updating tracking status: {str(e)}")
    
    gif_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

@app.route('/reply')
def mark_replied():
    email = request.args.get('email')
    tracking_id = request.args.get('id')
    
    print(f"Reply tracking: email={email}, tracking_id={tracking_id}")
    
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            
            if tracking_id:
                mask = (df['Tracking ID'] == tracking_id) & (df['Status'].isin(['not viewed', 'viewed']))
            else:
                mask = (df['Receiver Email'] == email) & (df['Status'].isin(['not viewed', 'viewed']))
            
            if mask.any():
                df.loc[mask, 'Status'] = 'replied'
                df.to_csv(LOG_FILE, index=False)
                print(f"Updated status to 'replied' for tracking_id: {tracking_id}")
                return jsonify({"status": "success", "message": "Reply tracked successfully"})
            else:
                print(f"No matching entry found for reply tracking: {tracking_id}")
                return jsonify({"status": "error", "message": "No matching entry found"})
                
        except Exception as e:
            print(f"Error updating reply status: {str(e)}")
            return jsonify({"status": "error", "message": str(e)})
    
    return jsonify({"status": "error", "message": "Log file not found"})

@app.route('/status')
def get_status():
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            stats = {
                "total_sent": len(df),
                "not_viewed": len(df[df['Status'] == 'not viewed']),
                "viewed": len(df[df['Status'] == 'viewed']),
                "replied": len(df[df['Status'] == 'replied'])
            }
            return jsonify(stats)
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify({"error": "Log file not found"})

if __name__ == '__main__':
    print("Starting email tracking server on port 5000...")
    print("Endpoints:")
    print("  /track - Track email opens")
    print("  /reply - Track email replies")
    print("  /status - Get tracking statistics")
    app.run(port=5000, debug=True)