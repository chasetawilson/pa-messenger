from flask import request, flash
from pa_messenger.forms import SendMessageForm
from pa_messenger.models import init_models_module
from pa_messenger.twilio import init_twilio_module
from pa_messenger.view_helpers import twiml, view
from flask import Blueprint, send_from_directory
from pa_messenger.twilio.twilio_services import TwilioServices
from flask_basicauth import BasicAuth


def construct_view_blueprint(app, db):
    SUBSCRIBE_COMMAND = "subscribe"
    UNSUBSCRIBE_COMMAND = "unsubscribe"

    views = Blueprint("views", __name__)

    init_twilio_module(app)
    init_models_module(db)
    basic_auth = BasicAuth(app)
    from pa_messenger.models.subscriber import Subscriber

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)


    @views.route('/', methods=["GET", "POST"])
    def home():
        return view('home')

    @views.route('/admin', methods=["GET", "POST"])
    @basic_auth.required
    def notifications():
        form = SendMessageForm()
        if request.method == 'POST' and form.validate_on_submit():
            subscribers = Subscriber.query.filter(Subscriber.subscribed).all()
            if len(subscribers) > 0:
                flash('Messages on their way!')
                twilio_services = TwilioServices()
                imgUrl = None
                if form.imageUrl.data:
                    imgUrl = form.imageUrl.data
                for s in subscribers:
                    twilio_services.send_message(s.phone_number, form.message.data, imgUrl)
            else:
                flash('No subscribers found!')

            form.reset()
            return view('notifications', form)

        return view('notifications', form)

    @views.route('/message', methods=["POST"])
    def message():
        subscriber = Subscriber.query.filter(Subscriber.phone_number == request.form['From']).first()
        if subscriber is None:
            subscriber = Subscriber(phone_number=request.form['From'])
            db.session.add(subscriber)
            if request.form['Body'].lower().startswith(SUBSCRIBE_COMMAND):
                output = _process_message(request.form['Body'], subscriber)
            else:
                output = "Thanks for contacting Montavilla EWS! Text 'subscribe' if you would like to receive updates via text message."
            db.session.commit()
        else:
            output = _process_message(request.form['Body'], subscriber)
            db.session.commit()

        twilio_services = TwilioServices()
        return twiml(twilio_services.respond_message(output))

    def _process_message(message, subscriber):
        output = "Sorry, we don't recognize that command. Available commands are: 'subscribe' or 'unsubscribe'."

        message = message.lower()

        if message.startswith(SUBSCRIBE_COMMAND) or message.startswith(UNSUBSCRIBE_COMMAND):
            subscriber.subscribed = message.startswith(SUBSCRIBE_COMMAND)

            if subscriber.subscribed:
                output = "You are now subscribed for updates."
            else:
                output = "You have unsubscribed from notifications. Text 'subscribe' to start receiving updates again"

        return output

    return views
