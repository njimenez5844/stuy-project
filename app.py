from flask import Flask, render_template, request, redirect
import online_test_method
import pandas as pd

app = Flask(__name__)
history_df = pd.DataFrame(columns=['Username', 'Question', 'Label'])


@app.route('/')
def home():
    return render_template('home.html', messages=[])


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        username = request.form['username']
        question = request.form['message']
        label = request.form['label']

        global history_df
        history_df = history_df.append({'Username': username, 'Question': question, 'Label': label},
                                       ignore_index=True)
        history_df.to_csv('data/history.csv', index=False)  # Save the dataframe to CSV

        return redirect('/history')

    return render_template('home.html', messages=[])


@app.route('/history')
def history():
    global history_df
    form_history = history_df.to_dict('records')
    return render_template('history.html', form_history=form_history)


@app.route('/send', methods=['POST'])
def send():
    messages = []
    message = request.form['message']
    messages.append(('user', message))
    # bot's response generated from our algorithm
    bot_response = online_test_method.online_test(message)
    messages.append(('bot', bot_response))
    return render_template('response.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)