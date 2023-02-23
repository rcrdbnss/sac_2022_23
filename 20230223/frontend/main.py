import uuid

from dao import DAO
from flask import Flask, render_template, request, redirect, session, url_for
from wtforms import Form, StringField, TextAreaField, validators

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

dao = DAO()


class MessageForm(Form):
    message = TextAreaField('message', [validators.length(min=1, max=100)])


class HashtagForm(Form):
    hashtag = StringField('hashtag', [validators.length(min=1)])

@app.route('/chirps', methods=['GET', 'POST'])
def chirps():
    if request.method == 'GET':
        return get_chirps()
    if request.method == 'POST':
        return post_chirps()

@app.route('/hashtag/<ht>', methods=['GET'])
def get_hashtag(ht):
    ms = dao.get_messages_with(ht)
    print(ms)
    messages = []
    if ms is not None:
        for m in ms:
            messages.append(dao.get_message(uuid.UUID(m)))
    session['messages'] = messages
    return render_template('hashtag.html', messages=session['messages'])


def get_chirps():
    message_form = MessageForm()
    hashtag_form = HashtagForm()
    return render_template("chirps_home.html", message_form=message_form, hashtag_form=hashtag_form)

def post_chirps():
    if 'message_form' in request.form:
        form = MessageForm(request.form)
        print(form.data)
        dao.add_message(form.data['message'])
        return redirect(url_for('chirps'))

    if 'hashtag_form' in request.form:
        form = HashtagForm(request.form)
        print(form.data)
        ht = form.data['hashtag']
        return redirect(f'/hashtag/{ht}')




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
    app.run('127.0.0.1', port=8081, debug=True)
