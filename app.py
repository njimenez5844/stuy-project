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
        return redirect('/history')
    return render_template('home.html', messages=[])

@app.route('/history')
def history():
    form_history = history_df.to_dict('records')
    return render_template('history.html', form_history=form_history)

@app.route('/send', methods=['POST'])
def send():
    global history_df
    #username = request.form['username']
    messages = []
    message = request.form['message']
    messages.append(('Question:', message))

    # bot's response generated from our algorithm
    bot_response = online_test_method.online_test(message)
    messages.append(('Label:', bot_response))
      
    history_df = history_df.append({'Username': 'keobkeig', 'Question': message, 'Label': bot_response},
                                    ignore_index=True)
    
    #To save the history of the chat in memory onto a csv file
    #history_df.to_csv('data/history.csv', index=False)  # Save the dataframe to CSV

    return render_template('response.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)