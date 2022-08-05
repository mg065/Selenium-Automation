from datetime import datetime
import requests
import turtle
from time import sleep

PROJECTS = {'ali': 'ALI', 'auto': 'Automation'}


def get_progress_report_email_subject(project=None):
    if not project:
        project = PROJECTS.get('ali')

    date_today = datetime.strftime(datetime.today().date(), "%B %dth, %Y")
    if datetime.today().date().day in [1, 21, 31]:
        _month = date_today.split(',')[0].split(' ').pop(0)
        _day = date_today.split(',')[0].split(' ')[-1].replace('th', 'st')
        _year = date_today.split(',').pop()
        date_today = f'{_month} {_day},{_year}'

    elif datetime.today().date().day in [2, 22]:
        _month = date_today.split(',')[0].split(' ').pop(0)
        _day = date_today.split(',')[0].split(' ')[-1].replace('th', 'nd')
        _year = date_today.split(',').pop()
        date_today = f'{_month} {_day},{_year}'

    elif datetime.today().date().day in [3, 23]:
        _month = date_today.split(',')[0].split(' ').pop(0)
        _day = date_today.split(',')[0].split(' ')[-1].replace('th', 'rd')
        _year = date_today.split(',').pop()
        date_today = f'{_month} {_day},{_year}'

    subject = f'{project} Progress Report - {date_today.replace(",", "")}'
    return subject, date_today


def get_progress_report_body_template(date_today, task_ref=None):
    if not task_ref:
        return
    body_template = f"""AssalamuAlaikum,\n
    Below you will find the progress report for {date_today}.\n\nTask: \n
    Ref: {task_ref}\nStatus: In progress\n\nUpdate:\n"""

    return body_template


def have_network_connection():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print(exception)
        return False


def show_netflix():

    # Part 1 : Initialize the module
    t = turtle.Turtle()
    t.speed(4)
    turtle.bgcolor("white")
    t.color("white")
    turtle.title('Netflix Logo')

    # Part 2 : Drawing the black background
    t.up()
    t.goto(-80, 50)
    t.down()
    t.fillcolor("black")
    t.begin_fill()

    t.forward(200)
    t.setheading(270)
    s = 360
    for i in range(9):
        s = s - 10
        t.setheading(s)
        t.forward(10)

    t.forward(180)
    s = 270
    for i in range(9):
        s = s - 10
        t.setheading(s)
        t.forward(10)

    t.forward(200)
    s = 180
    for i in range(9):
        s = s - 10
        t.setheading(s)
        t.forward(10)

    t.forward(180)
    s = 90
    for i in range(9):
        s = s - 10
        t.setheading(s)
        t.forward(10)
    t.forward(30)
    t.end_fill()

    # Part 3 : Drawing the N shape
    t.up()
    t.color("black")
    t.setheading(270)
    t.forward(240)
    t.setheading(0)
    t.down()
    t.color("red")
    t.fillcolor("#E50914")
    t.begin_fill()
    t.forward(30)
    t.setheading(90)
    t.forward(180)
    t.setheading(180)
    t.forward(30)
    t.setheading(270)
    t.forward(180)
    t.end_fill()
    t.setheading(0)
    t.up()
    t.forward(75)
    t.down()
    t.color("red")
    t.fillcolor("#E50914")
    t.begin_fill()
    t.forward(30)
    t.setheading(90)
    t.forward(180)
    t.setheading(180)
    t.forward(30)
    t.setheading(270)
    t.forward(180)
    t.end_fill()
    t.color("red")
    t.fillcolor("red")
    t.begin_fill()
    t.setheading(113)
    t.forward(195)
    t.setheading(0)
    t.forward(31)
    t.setheading(293)
    t.forward(196)
    t.end_fill()
    t.hideturtle()
    sleep(10)

    return
