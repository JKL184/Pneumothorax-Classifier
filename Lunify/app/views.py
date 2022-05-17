"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from __future__ import division, print_function
from app import app ,db, login_manager
from flask import render_template, request, redirect, url_for, flash,g,send_from_directory
from app.forms import LoginForm,RegisterForm,settingsForm,resultsForm,searchForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import UserProfile,Result,Scan,Setting
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import io
import os 
import matplotlib.pyplot as plt 
import tensorflow as tf 
import numpy as np 
import time
import cv2
import pydicom
from PIL import Image
from build_image import read_image,classify_decode
from build_models import build_segment
from prediction import prediction 
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

classify_weights_path = "../../models stuff/chexnet_model_new2.h5"
segment_weights_path = '../../models stuff/B2best_Double_Unet_new.hdf5'
pred = prediction(classify_weights_path,segment_weights_path)
# ###
# Routing for your application.
###

Mailemail=""



# send our email message 'msg' to our boss
def message(subject="Python Notification",
			text="", img=None,
			attachment=None):
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg.attach(MIMEText(text))
	if img is not None:	
		if type(img) is not list:	
			img = [img]
		for one_img in img:	
			img_data = open(one_img, 'rb').read()
			msg.attach(MIMEImage(img_data,
								name=os.path.basename(one_img)))
	if attachment is not None:
		if type(attachment) is not list:
			attachment = [attachment]
		for one_attachment in attachment:
			with open(one_attachment, 'rb') as f:
				file = MIMEApplication(f.read(),name=os.path.basename(one_attachment))
			file['Content-Disposition'] = f'attachment;\
			filename="{os.path.basename(one_attachment)}"'
			msg.attach(file)
	return msg
#smtp.quit()


@app.route('/home')
def home():
    #Render website's home page.
    return render_template('about.html')

def dicom2png(file):
    '''
    This function inputs the path of the image to be read
    and create a .png format for the same image and store in the path created.
    '''
    ds = pydicom.read_file(str(file))
    img = ds.pixel_array
    # formatting the image to make training the network faster.
    img = cv2.resize(img, (256,256) )
    fname = file.replace('.dcm','.png')
    cv2.imwrite(fname, img)

def jpg2png(file):
    im1 = cv2.imread(str(file))
    # formatting the image to make training the network faster.
    img = cv2.resize(im1, (256,256) )
    fname = file.replace('.jpg','.png')
    cv2.imwrite(fname, img)

@app.route('/test', methods=['GET', 'POST']) 
def main_page():
    if current_user.is_authenticated():
        g.user = current_user.get_id()
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        name,extension=os.path.splitext(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if extension==".dcm":
            dicom2png(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = filename.replace('.dcm','.png')
        if extension==".jpg":
            jpg2png(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = filename.replace('.jpg','.png')
        date=datetime.date.today()
        scan=Scan(photo=filename,user_id=g.user,date_scanned=date)
        if scan is not None:
            db.session.add(scan)
            db.session.commit()
        # Call the message function
        
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/prediction/<filename>', methods = ['GET', 'POST']) 
def prediction(filename):
    if current_user.is_authenticated():
        g.user = current_user.get_id()

#     # Make prediction
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    scan=filename
    name,extension=os.path.splitext(filename)
    classify_output, pred_mask = pred.Predict(image_path)
    print("Classification Output : ",classify_output)
    if(classify_output> 0.5):
        print("Classifier Prediction Confidence : {}%".format(classify_output*100))
        print('segment printing')
        pred_mask1 = np.squeeze(pred_mask[:,:,:,1])
        plt.imsave('predicted_mask.png', pred_mask1)
        background = Image.open(image_path)
        overlay = Image.open('predicted_mask.png')
        background = background.convert("RGBA")
        overlay = overlay.convert("RGBA")
        new_img = Image.blend(background, overlay, 0.3)
        new_graph_name = "Output_pos_" +name  + ".png"
        for filename in os.listdir('app/static/outputs/'):
            if filename.startswith("Output_pos_" +name ):  # not to remove other images
                os.remove('app/static/outputs/' + filename)
        new_img.save(os.path.join("app/static/outputs/", new_graph_name))
        classify_result = classify_output*100
        classify_text = 'Pneumothorax Detected'
        identification="Positive"
        # #EMAIL
        # smtp = smtplib.SMTP('smtp.gmail.com', 587)
        # smtp.ehlo()
        # smtp.starttls()
        # smtp.login('Lungify@gmail.com', 'Lungify123')
        # msg = message("Pneumothorax Detected", "A Pneumothorax has been detected",
        #             img=os.path.join("app/static/", new_graph_name))
        # # Make a list of emails, where you wanna send mail
        # to = [Mailemail,"jokal@yopmail.com"]
        # # Provide some data to the sendmail function!
        # smtp.sendmail(from_addr="Lungify@gmail.com",
        #             to_addrs=to, msg=msg.as_string())
    else:
        print('No Pneumothorax Detection...!')
        no_confidence = 1 - classify_output
        print('Classifier Prediction Confidence : {}%'.format(no_confidence*100))
        classify_result = no_confidence*100
        identification="Negative"
        classify_text = 'No Pneumothorax Detected'
        background = Image.open(image_path)
        new_graph_name = "Output_neg_" + name  + ".png"
        for filename in os.listdir('app/static/outputs/'):
            if filename.startswith('Output_neg_'+filename):  # not to remove other images
                os.remove('app/static/outputs/' + filename)
        background.save((os.path.join("app/static/outputs/", new_graph_name)))	
    form = resultsForm()
    form.confidence.data=classify_result
    form.img.data=new_graph_name
    form.identification.data=identification
    #print(type(classify_result))
    return render_template('basepd.html',segmented_image = new_graph_name, result = classify_result, review_text = classify_text,identify=identification,form=form)

@app.route('/prediction/add', methods = ['GET', 'POST']) 
def addresult():
    if current_user.is_authenticated():
        g.user = current_user.get_id()
    form = resultsForm()
    if request.method == "POST":
        img = form.img.data
        confidence = form.confidence.data
        identification = form.identification.data
        Pname=form.patient.data
        location=form.location.data
        date=datetime.date.today()
        result=Result(photo=img,location=location,patname=Pname,empid=g.user,date_scanned=date,identification=identification,confidence=confidence,user_id=g.user)
        if result is not None:
            db.session.add(result)
            db.session.commit()
            
        #if (identification=="Positive"):
            sett=Setting.query.filter_by(user_id=g.user).first()
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login('Lungify@gmail.com', 'Lungify123')
            body="Patient Name - "+Pname+" \n System Identification - "+identification+" \n Location - "+location+" \n Employee ID - "+g.user+" \n Date Scanned - "+date.strftime("%d %b, %Y ")
            msg = message("Pneumothorax Detection Result - "+Pname, body,
                        img=os.path.join("app/static/outputs/", img))
            # Make a list of emails, where you wanna send mail
            to = [sett.email,"jokal@yopmail.com"]
            # Provide some data to the sendmail function!
            smtp.sendmail(from_addr="Lungify@gmail.com",
                        to_addrs=to, msg=msg.as_string())
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    if current_user.is_authenticated():
        g.user = current_user.get_id()
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        name,extension=os.path.splitext(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if extension==".dcm":
            dicom2png(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = filename.replace('.dcm','.png')
        if extension==".jpg":
            jpg2png(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = filename.replace('.jpg','.png')
        if extension==".jpeg":
            jpg2png(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = filename.replace('.jpeg','.png')
        date=datetime.date.today()
        scan=Scan(photo=filename,user_id=g.user,date_scanned=date)
        if scan is not None:
            db.session.add(scan)
            db.session.commit()
        
        return redirect(url_for('prediction', filename=filename))
    return render_template('upload.html')
    
@app.route('/settings', methods=["GET", "POST"])
@login_required 
def settings():
    if current_user.is_authenticated():
        g.user = current_user.get_id()
    sett=Setting.query.filter_by(user_id=g.user).first()
    form = settingsForm()
    if request.method == "POST":
        Mailemail=form.email.data
        size= form.size.data
        if sett is not None:
            sett.email=Mailemail
            sett.size=size
            db.session.commit()
        return render_template('settings.html',form=form,sett=sett)
    if sett is None:
        sett=Setting(email= "",size=0,user_id=g.user)
        db.session.add(sett)
        db.session.commit()

    return render_template('settings.html',form=form,sett=sett)



@app.route("/archive", methods=["GET", "POST"])
def archive():
    form=searchForm()
    results=Result.query.order_by(Result.id.desc()).all()
    if request.method == "POST":
        if form.location.data=="":
            location=form.location.data
        else:
            location="%{}%".format(form.location.data)
        if form.patient.data=="":
            patname=form.patient.data
        else:
            patname="%{}%".format(form.patient.data)
        emp=form.employee.data
        datesc=form.date.data
        iden=form.identification.data
        print([location,patname,emp,datesc,iden])
        search_results= Result.query.filter((Result.location.like(location)|Result.patname.like(patname)|Result.empid.like(emp)|Result.identification.like(iden)|Result.date_scanned.is_(datesc)))
        form=searchForm()
        print(("" ==location == patname == emp == patname== iden))
        print(datesc==None)
        if ("" ==location == patname == emp == patname== iden) & (datesc==None):
            return render_template('archive.html', results=results,form=form)
        else:
            return render_template('archive.html', results=search_results,form=form)
    
    return render_template('archive.html', results=results,form=form)

@app.route("/archive/<resultid>")
def get_result(resultid):
    result = Result.query.filter_by(id=resultid).first()
    return render_template('result.html', result=result)

@app.route("/outputs/<filename>")
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['OUTPUT_FOLDER']), filename)

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
            # Get the username and password values from the form.
            fname=form.fname.data
            lname=form.lname.data
            email=form.email.data
            password=form.password.data
            user = UserProfile(first_name=fname,last_name=lname, email=email,password=password)
            if user is not None :
                db.session.add(user)
                db.session.commit()
            # get user id, load into session
                return redirect(url_for("login"))
            else:
                flash('User already exists ', 'danger')
    return render_template("register.html", form=form)



@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        if form.email.data:
            email=form.email.data
            password=form.password.data
            user = UserProfile.query.filter_by(email=email).first()
            if user is not None and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("about"))
            else:
                flash('Email or Password is incorrect.', 'danger')
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('login'))
    
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


@app.route('/account/')
def account():
    """Render the website's about page."""
    return render_template('account.html')


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
