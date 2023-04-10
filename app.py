from flask import Flask, render_template, request
import online_test_method

app = Flask(__name__)

# input machine learning algorithm here 
# bot = pipeline('text-generation', model='model_name')

@app.route('/')
def home():
    return render_template('home.html', messages = [])

@app.route('/send', methods=['POST'])
def send():
    messages = []
    message = request.form['message']
    messages.append(('user', message))
    # bot's response generated from our algorithm 
    bot_response = online_test_method.online_test(message)
    messages.append(('bot', bot_response))
    return render_template('home.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
