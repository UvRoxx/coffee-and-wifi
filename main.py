from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


def create_rating(rating_emoji):
    result = ['✘']
    for i in range(1, 6):
        temp = ""
        for j in range(0, i):
            temp += rating_emoji
        result.append(temp)
    return result


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location', validators=[DataRequired(), URL()])
    opening_time = StringField('Opening Time', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=create_rating("☕️"), validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Rating", choices=create_rating("💪"), validators=[DataRequired()])
    power_rating = SelectField("Power Rating", choices=create_rating("🔌️"), validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", 'a') as data:
            new_data = f"{form.cafe.data}, {form.location.data}, {form.opening_time.data}, {form.closing_time.data},{form.coffee_rating.data}, {form.wifi_rating.data}, {form.power_rating.data}\n"
            data.write(new_data)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
