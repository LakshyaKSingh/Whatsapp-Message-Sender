from flask import Flask, render_template, request, redirect, url_for, flash
import time
import webbrowser
import pyautogui
import pyperclip

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def send_whatsapp_message(phone_number, message, num_times, delay_seconds):
    try:
        chat_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        webbrowser.open(chat_url)
        time.sleep(15)  # Wait for WhatsApp Web to load

        # Send first message
        pyautogui.press('enter')

        for i in range(1, num_times):
            time.sleep(delay_seconds)
            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')

    except Exception as e:
        print(f"Error: {e}")
        raise e

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone = request.form['phone']
        message = request.form['message']
        count = int(request.form['count'])
        delay = int(request.form['delay'])

        try:
            send_whatsapp_message(phone, message, count, delay)
            flash("Messages sent successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect(url_for('index'))

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
