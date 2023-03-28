from flask import Flask, render_template, request

app = Flask(__name__)
messages = []

# input machine learning algorithm here 
# bot = pipeline('text-generation', model='model_name')

# for testing purposes 
def generate_bot_response(message):
    return 'Hi, how can I help you?'

@app.route('/')
def home():
    return render_template('home.html', messages=messages)

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    messages.append(('user', message))
    # bot's response generated from our algorithm 
    bot_response = generate_bot_response(message)
    messages.append(('bot', bot_response))
    return render_template('home.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
