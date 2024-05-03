from matplotlib import pyplot as plt
from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Schedule, User
from app.classes.forms import ScheduleForm, ConsentForm
from flask_login import login_required
import datetime as dt

@app.route('/consent', methods=['GET', 'POST'])
def consent():
    form = ConsentForm()
    if form.validate_on_submit():
        if form.consent.data == "True":
            consent = True
        else:
            consent = False
        current_user.update(
            consent = consent,
            adult_fname = form.adult_fname.data,
            adult_lname = form.adult_lname.data,
            adult_email = form.adult_email.data
        )
        return redirect(url_for('myProfile'))

    form.consent.process_data(current_user.consent)
    form.adult_fname.data = current_user.adult_fname
    form.adult_lname.data = current_user.adult_lname
    form.adult_email.data = current_user.adult_email
    return render_template("consentform.html", form=form)


@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/schedule/new', methods=['GET', 'POST'])
@login_required
def scheduleNew():
    form = ScheduleForm()
    if form.validate_on_submit():
        startDT = dt.datetime.combine(form.schedule_date.data, form.starttime.data)
        endDT = dt.datetime.combine(form.wake_date.data, form.endtime.data)
        diff = endDT - startDT
        hours = diff.seconds/60/60
        newSchedule = Schedule(
            hours = hours,
            scheduleer = current_user,
            rating = form.rating.data,
            start = startDT,
            end = endDT,
            feel = form.feel.data,
            minstoschedule = form.minstoschedule.data,
        )
        newSchedule.save()
        return redirect(url_for("schedule",scheduleId=newSchedule.id))
    
    if form.submit.data:
        if form.rating.data == 'None':
            form.rating.errors = ['Required']
        if form.feel.data == 'None':
            form.feel.errors = ['Required']
        
    return render_template("scheduleform.html",form=form)

@app.route('/schedule/edit/<scheduleId>', methods=['GET', 'POST'])
@login_required

def scheduleEdit(scheduleId):
    form = ScheduleForm()
    editSchedule = Schedule.objects.get(id=scheduleId)

    if editSchedule.scheduleer != current_user:
        flash("You can't edit a schedule you don't own.")
        return redirect(url_for('schedules'))
    
    if form.validate_on_submit():
        startDT = dt.datetime.combine(form.schedule_date.data, form.starttime.data)
        endDT = dt.datetime.combine(form.wake_date.data, form.endtime.data)
        diff = endDT - startDT
        hours = diff.seconds/60/60

        editSchedule.update(
            hours = hours,
            rating = form.rating.data,
            start = startDT,
            end = endDT,
            feel = form.feel.data,
            minstoschedule = form.minstoschedule.data
        )
        return redirect(url_for("schedule",scheduleId=editSchedule.id))
    
    form.schedule_date.process_data(editSchedule.start.date())
    form.starttime.process_data(editSchedule.start.time())
    form.wake_date.process_data(editSchedule.end.date())
    form.endtime.process_data(editSchedule.end.time())
    form.rating.process_data(editSchedule.rating)
    form.feel.process_data(editSchedule.feel)
    form.minstoschedule.data = editSchedule.minstoschedule
    return render_template("scheduleform.html",form=form)

@app.route('/schedule/<scheduleId>')
@login_required

def schedule(scheduleId):
    thisSchedule = Schedule.objects.get(id=scheduleId)
    return render_template("schedule.html",schedule=thisSchedule)

@app.route('/schedules')
@login_required

def schedules():
    schedules = Schedule.objects()
    return render_template("schedules.html",schedules=schedules)

def scheduleDelete(scheduleId):
    delSchedule = Schedule.objects.get(id=scheduleId)
    scheduleDate = delSchedule.schedule_date
    delSchedule.delete()
    flash(f"schedule with date {scheduleDate} has been deleted.")
    return redirect(url_for('schedules'))

#@app.route('/schedulegraph')
#@login_required

#def schedulegraph():
    schedules = schedule.objects()


    hours = []
    dates = []
    colors = []
    for schedule in schedules:
        hours.append(schedule.hours)
        dates.append(schedule.start.date())   
        if schedule.rating >=4:
            colors.append('green')
        elif schedule.rating == 3:
            colors.append('yellow')
        else:
            colors.append('red')
    
    plt.switch_backend('Agg') 
    fig, ax = plt.subplots()
    
    ax.scatter(dates, hours, marker='o', c=colors)


    ax.legend()
    plt.yticks(hours)
    plt.xticks(dates, rotation=45)
    plt.gcf().set_size_inches(10, 5)
    fig.savefig("app/static/graphs/schedule.png", bbox_inches="tight")
    fig.show()
    return render_template('schedulegraph.html',images=['schedule.png'])