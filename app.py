from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from api.gemini_service import GeminiService
from utils.helpers import Helpers

# ✅ NEW IMPORTS FOR EMAIL
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# ✅ EMAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

mail = Mail(app)

# Initialize services
gemini_service = GeminiService()
helpers = Helpers()

# Store generation history
generation_history = []


@app.route('/')
def index():
    return render_template('index.html')


# ✅ NEW PAGES ROUTES
@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


# ✅ MAIN GENERATE ROUTE
@app.route('/api/generate', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({
                "success": False,
                "message": "No prompt provided"
            }), 400

        prompt = data['prompt'].strip()
        style = data.get('style', 'No specific style')

        if not helpers.validate_prompt(prompt):
            return jsonify({
                "success": False,
                "message": "Invalid prompt"
            }), 400

        success, result = gemini_service.generate_image(prompt, style)

        if success:
            image_id = helpers.generate_image_id(prompt, style)

            history_entry = {
                'id': image_id,
                'prompt': prompt,
                'style': style
            }
            generation_history.append(history_entry)

            if len(generation_history) > 50:
                generation_history.pop(0)

            return jsonify({
                "success": True,
                "image": f"data:image/jpeg;base64,{result}",
                "prompt": prompt,
                "style": style,
                "image_id": image_id
            })

        else:
            return jsonify({
                "success": False,
                "message": f"Generation failed: {result}"
            }), 500

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ✅ CONTACT FORM API (EMAIL SENDING ADDED 🔥)
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.json

        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # ✅ CREATE EMAIL
        msg = Message(
            subject=f"New Contact: {subject}",
            sender=os.getenv('EMAIL_USER'),
            recipients=[os.getenv('EMAIL_USER')]
        )

        msg.body = f"""
New Contact Message 🚀

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
        """

        # ✅ SEND EMAIL
        mail.send(msg)

        return jsonify({
            "success": True,
            "message": "Message sent successfully! We'll get back to you soon."
        })

    except Exception as e:
        app.logger.error(f"Contact form error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to send message. Please try again."
        }), 500


# ✅ HEALTH CHECK
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AI Image Generator'
    })


# ✅ HISTORY
@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({
        "success": True,
        "history": generation_history
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)