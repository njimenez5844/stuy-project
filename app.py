from flask import Flask, render_template, request, redirect
import online_test_method
import pandas as pd

app = Flask(__name__)

history_df = pd.DataFrame(columns=['Username', 'Question', 'Label'])
users_df = pd.DataFrame(columns=['username', 'password'])
#users_df = pd.read_csv('data/users.csv')

current_user = None
current_username = None

#defaults onto signin page
@app.route('/')
def signin_page():
    return redirect('/signin')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        un = request.form['username']
        pw = request.form['password']

        # pre-existing user
        user = users_df[(users_df['username'] == un) & (users_df['password'] == pw)]
        if not user.empty:
            global current_user
            current_user = user.iloc[0]
            global current_username
            current_username = un
            return redirect('/home')

        return render_template('signin.html', error=True)

    return render_template('signin.html', error=False)

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        un = request.form['username']
        pw = request.form['password']

        global users_df
        if un in users_df['username'].values:
            return render_template('create.html', error=True)

        new = pd.DataFrame({'username': [un], 'password': [pw]})
        users_df = users_df.append(new, ignore_index=True)
        # To save the user data in memory onto a csv file
        #users_df.to_csv('data/users.csv', index=False)  

        return redirect('/signin')

    return render_template('create.html', error=False)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect('/history')
    return render_template('home.html', messages=[])

@app.route('/history')
def history():
    form_history = history_df.to_dict('records')
    return render_template('history.html', form_history=form_history)

@app.route('/ask', methods=['GET', 'POST'])
def ask_problem():
    if request.method == 'POST':
        subject = request.form['subject']

        prompt = f"Ask a high school {subject} word problem. Only include the problem. Don't show explanations. Don't show the answer. Do it in 2 sentences."
        generated_question = online_test_method.bard(prompt)['content'].split('>')[1]
        generated_question = generated_question.split('?')[0] + '?'
       
        global history_df
        history_df = history_df.append({'Username': current_user.iloc[0], 'Question': generated_question, 'Label': subject},
                                       ignore_index=True)
        # Redirect to the response page with the generated prompt
        return redirect(f'/response?question={generated_question}')

    return render_template('ask.html')

@app.route('/response')
def show_response():
    question = request.args.get('question', '')

    # Render the response page with the prompt
    return render_template('bard_response.html', question=question)

@app.route('/send', methods=['POST'])
def send():
    global history_df
    # username = request.form['username']
    messages = []
    message = request.form['message']
    messages.append(('Question', message))

    # bot's response generated from our algorithm
    bot_response = online_test_method.online(message)
    messages.append(('Label', bot_response))

    history_df = history_df.append({'Username': current_user.iloc[0], 'Question': message, 'Label': bot_response},
                                   ignore_index=True)

    # To save the history of the chat in memory onto a csv file
    # history_df.to_csv('data/history.csv', index=False)  # Save the dataframe to CSV

    return render_template('response.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)