from flask_wtf import Form
from werkzeug.datastructures import MultiDict
from wtforms import TextField, StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class SendMessageForm(Form):
    message = StringField('Message*', validators=[DataRequired(message="Message is required")], widget=TextArea())
    imageUrl = TextField('Image URL', validators=[])

    def reset(self):
        blankData = MultiDict([('message', ''), ('imageUrl', '')])
        self.process(blankData)
