from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for flashing messages

API_KEY = 'M7zmke8K8fHV'  # Your TextMeBot API key
API_URL = 'https://api.textmebot.com/send.php'

def add_invisible_char(message, index):
    # Adds zero-width spaces to make messages technically different
    return message + ("\u200B" * index)

def send_whatsapp_message(phone, message):
    try:
        payload = {
            'recipient': phone,
            'apikey': API_KEY,
            'text': message
        }
        response = requests.get(API_URL, params=payload)
        if response.status_code == 200:
            if "error" in response.text.lower():
                return f"CallMeBot error: {response.text}"
            return "Message sent successfully."
        else:
            return f"Error: Status code {response.status_code}"
    except Exception as e:
        return f"Exception: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone = request.form['phone']
        message = request.form['message']
        count = int(request.form['count'])
        delay = int(request.form['delay'])

        for i in range(count):
            unique_message = add_invisible_char(message, i)
            result = send_whatsapp_message(phone, unique_message)
            if "successfully" in result.lower():
                flash(f"Message {i+1} sent successfully.", "success")
            else:
                flash(f"Message {i+1} failed: {result}", "danger")
            if i < count - 1:
                time.sleep(delay)

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
