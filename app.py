from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "you'll-never-guess"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RES_KEY = "responses"

@app.route('/')
def start_page():
    """Begins survey"""
    
    return render_template('start.html', survey = survey)

@app.route('/start', methods=['POST'])
def start_survey():
    """Resets resonses"""
    
    session[RES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_question():
    """Saves answers to list and redirects to nect question """
    
    choice = request.form['answer']
    responses = session[RES_KEY]
    responses.append(choice)
    session[RES_KEY] = responses
    
    if(len(responses) == len(survey.questions)):
        return redirect('/finish')
    else:
        return redirect(f'/questions/{len(responses)}')
    
@app.route('/questions/<int:id>')
def show_question(id):
    """Display the correct question"""
    
    responses = session.get(RES_KEY)
    if(responses is None):
        return redirect('/')
    
    if(len(responses) != id):
        flash(f'Question id: {id} is not a valid id.')
        return redirect(f'/questions/{len(responses)}')
    
    if(len(responses) == len(survey.questions)):
        return redirect('/finish')
    
    question = survey.questions[id]
    return render_template('question.html', question_num = id, question = question)

@app.route('/finish')
def finish_survey():
    """Shows finish page once survey is complete"""
    
    return render_template('finish.html')