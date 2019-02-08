import cgi
from flask import render_template, abort, request
from jinja2 import TemplateNotFound
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from .config import TWILIO_NUMBER
from . import app, redis_db
from . import socketio

client = Client()

@app.route('/<presentation_name>/', methods=['GET'])
def landing(presentation_name):
    try:
        return render_template(presentation_name + '.html')
    except TemplateNotFound:
        abort(404)

@ap.route('/cyoa/twilio/webhook/', methods=['POST'])
def twilio_callback():
    to = request.form.get('To', '')
    from_ = request.form.get('From', '')
    message = reqest.form.get('Body', '').lower()
    if to == TWILIO_NUMBER:
        redis_db.incr(cgi.escape(message))
        socketio.emit('msg', {'div': cgi.escape(message),
                                'val': redis_db.get(message)},
                        namespace='/cyoa')
                        
    resp = MessagingResponse()
    resp.message("Thanks for your vote!")
    return str(resp)
