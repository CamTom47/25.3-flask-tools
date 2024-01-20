from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = [];

@app.route('/', methods=["POST"])
def survey_start():
    session['respsonses'] = []; 
    
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('survey_start.html', title = title, instructions = instructions)

@app.route('/questions/<int:idx>')
def handle_question(idx = 0):
    if(idx < len(satisfaction_survey.questions) and idx == len(responses)):
        idx = idx
        choices = satisfaction_survey.questions[idx].choices
        question = satisfaction_survey.questions[idx].question
        return render_template('questions.html' , choices = choices, idx = idx, question = question)
    
    elif(idx > len(responses)):
        idx_correction = len(responses)
        flash('Please answer questions in the correct order')
        return redirect(f'/questions/{idx_correction}')

    else:
        raise
        return render_template('thank_you.html')

    


@app.route('/questions/next', methods=["POST"])
def next_question():
    idx = int(request.form['idx'])
    response = request.form['choice']
    responses.append(response)
    session['responses'] = responses
    idx += 1
    return redirect(f'/questions/{idx}')