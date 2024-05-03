from app import app
from app.utils.secrets import getSecrets
import requests
from flask import render_template, flash, redirect, url_for
import requests
from flask_login import current_user
from app.classes.data import Hangout
from app.classes.forms import HangoutForm
from flask_login import login_required
import datetime as dt

@app.route('/hangout/map')
@login_required
def hangoutMap():

    hangouts = Hangout.objects()

    return render_template('hangoutlocator.html',hangouts=hangouts)

@app.route('/hangout/list')
@login_required
def hangoutList():

    hangouts = Hangout.objects()

    return render_template('hangouts.html',hangouts=hangouts)


@app.route('/hangout/<hangoutID>')
@login_required
def hangout(hangoutID):

    thisHangout = Hangout.objects.get(id=hangoutID)

    return render_template('hangout.html',hangout=thisHangout)


@app.route('/hangout/delete/<hangoutID>')
@login_required
def hangoutDelete(hangoutID):
    deleteHangout = Hangout.objects.get(id=hangoutID)

    deleteHangout.delete()
    flash('The Hangout was deleted.')
    return redirect(url_for('hangoutList'))

def updateLatLon(hangout):
    # get your email address for the secrets file
    secrets=getSecrets()
    # call the maps API with the address
    url = f"https://nominatim.openstreetmap.org/search?street={hangout.streetAddress}&city={hangout.city}&state={hangout.state}&postalcode={hangout.zipcode}&format=json&addressdetails=1&email={secrets['MY_EMAIL_ADDRESS']}"
    # get the response from the API
    r = requests.get(url)
    # Find the lat/lon in the response
    try:
        r = r.json()
    except:
        flash("unable to retrieve lat/lon")
        return(hangout)
    else:
        if len(r) != 0:
            # update the database
            hangout.update(
                lat = float(r[0]['lat']),
                lon = float(r[0]['lon'])
            )
            flash(f"hangout lat/lon updated")
            return(hangout)
        else:
            flash('unable to retrieve lat/lon')
            return(hangout)

@app.route('/hangout/new', methods=['GET', 'POST'])
@login_required
def hangoutNew():
    form = HangoutForm()

    if form.validate_on_submit():

        newHangout = Hangout(
            name = form.name.data,
            streetAddress = form.streetAddress.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            activites = form.activites.data,
            #groupRating = form.groupRating.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow,
        )
        newHangout.save()

        newHangout = updateLatLon(newHangout)

        import requests

        return redirect(url_for('hangout',hangoutID=newHangout.id))

    return render_template('hangoutform.html',form=form)

@app.route('/hangout/edit/<hangoutID>', methods=['GET', 'POST'])
@login_required
def hangoutEdit(hangoutID):
    editHangout = Hangout.objects.get(id=hangoutID)

    if current_user != editHangout.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('hangout',hangoutID=hangoutID))

    form = HangoutForm()
    if form.validate_on_submit():
        editHangout.update(
            name = form.name.data,
            streetAddress = form.streetAddress.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,     
            rating = form.rating.data,       
            activites = form.activites.data,
            
            
            #groupRating = form.groupRating.data,
            modifydate = dt.datetime.utcnow
        )
        editHangout = updateLatLon(editHangout)
        return redirect(url_for('hangout',hangoutID=hangoutID))

    form.name.data = editHangout.name
    form.streetAddress.data = editHangout.streetAddress
    form.city.data = editHangout.city
    form.state.data = editHangout.state
    form.zipcode.data = editHangout.zipcode
    form.rating.data = editHangout.rating
    form.activites.data = editHangout.activites
    #form.groupRating.data=current_user.groupRating

    return render_template('hangoutform.html',form=form)
