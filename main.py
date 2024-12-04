from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
import os
import math
from werkzeug.utils import secure_filename

 
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/comeback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

with open('config.json','r') as c:
    govind= json.load(c)["govind"]

app.config['Upload_Folder']=govind['upload_location']

app.secret_key = 'super-secret-key'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=govind['Username'],
    MAIL_PASSWORD=govind['Password']
    )
mail=Mail(app)

class contacts(db.Model):
     __tablename__ = 'contact'
     sNo=db.Column(db.Integer,primary_key=True)
     Name=db.Column(db.String(20),nullable= False)
     email=db.Column(db.String(20),nullable= False)
     phone_no=db.Column(db.Integer,nullable= False)
     message=db.Column(db.String(400),nullable= False)
     date=db.Column(db.DateTime,nullable=True)

class logins(db.Model):
     __tablename__ = 'login'
     sNo=db.Column(db.Integer,primary_key=True)
     userName=db.Column(db.String(20),nullable= False)
     email=db.Column(db.String(20),nullable= False)
     password=db.Column(db.String(20),nullable= False)
     date_created=db.Column(db.DateTime,nullable=True)

class Posts(db.Model):
     __tablename__ = 'posts'
     sNo=db.Column(db.Integer,primary_key=True)
     title=db.Column(db.String(200),nullable= False)
     subheading=db.Column(db.String(400),nullable= True)
     content=db.Column(db.String(4000),nullable= False)
     slug=db.Column(db.String,nullable= False)
     img_file=db.Column(db.String(20),nullable= True)
     date=db.Column(db.DateTime,nullable=True)
    
class comments(db.Model):
     __tablename__ = 'comment'
     Sno=db.Column(db.Integer,primary_key=True)
     Title=db.Column(db.String(500),nullable= False)
     subheading=db.Column(db.String(500),nullable= False)
     content=db.Column(db.String(500),nullable= False)
     Date=db.Column(db.DateTime,nullable=True)


@app.route('/')
def home():
    posted=Posts.query.filter_by().all()
    img1= url_for('static', filename='assets/img/blog.jpg')


#pagination method
    last = math.ceil(len(posted)/int(govind['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posted = posted[(page-1)*int(govind['no_of_posts']):(page-1)*int(govind['no_of_posts'])+ int(govind['no_of_posts'])]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)


    
    return render_template('index.html', image_url=img1, govind=govind, posted=posted, prev=prev, next=next)

@app.route('/about')
def about():
    img2= url_for('static', filename='assets/img/aboutme.jpg')
    return render_template('about.html', image_url=img2)

@app.route("/uploader", methods=['GET', 'POST'])
def upload():
    if('user' in session and session['user']==govind['nameuser']):
        if request.method=='POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['Upload_Folder'], secure_filename(f.filename)))
            return "Uploaded successfully!"


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/admin')


@app.route('/Comeback', methods=['GET', 'POST'])
def come():
    if(request.method=='POST'):
        name=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        entry=logins(userName=name,email=email,password=password,date_created= datetime.now())  
        db.session.add(entry)
        db.session.commit()
    img= url_for('static', filename='assets/img/login.jpeg')
    return render_template('come.html',image_url=img)

@app.route('/admin', methods=['GET','POST'])
def dash():
    img= url_for('static', filename='assets/img/admin.webp')

    if('user' in session and session['user']==govind['nameuser']):
        img1= url_for('static', filename='assets/img/admin3.jpg')
        posted = Posts.query.all()
        last_login = session.get('last_login')
        return render_template('dashboard.html',govind=govind,img_url=img1,posted=posted,last_login=last_login)

    if(request.method=='POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        if username==govind['nameuser'] and password==govind['passcode']:
            img1= url_for('static', filename='assets/img/admin3.jpg')
            posted = Posts.query.all()

            last_login_time=session.get('last_login')
            current_login_time = datetime.now().strftime('%H:%M:%S %Y-%m-%d')

            session['user']=username
            
            session['last_login'] = current_login_time  # Store old time in 'previous_login'
            
            return render_template('dashboard.html',govind=govind,img_url=img1,posted=posted,last_login=last_login_time)
   
    return render_template('admin.html',image_url=img)


@app.route('/post')
def explore():
    img3= url_for('static', filename='assets/img/explore.jpg')
    return render_template('explore.html',image_url=img3)


@app.route("/post/<string:post_slug>", methods=['GET', 'POST'])
def post_ext(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    image_url = url_for('static', filename='assets/img/' + post.img_file)

    if(request.method=='POST'):
        content=request.form.get('content')
        sno=post.sNo
        title=post.title
        sub=post.subheading
        entry=comments(Sno=sno,Title=title,subheading=sub,content=content)
        db.session.add(entry)
        db.session.commit()
        return render_template('success.html',post=post)

    return render_template('post.html',govind=govind, post=post,image_url=image_url)



@app.route("/contact", methods= ['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry=contacts(Name=name,email=email,phone_no=phone,message=message,date= datetime.now())  
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Message_from_yout_web',
                           sender=email, # not of use
                           recipients=['12312@gmail.com', govind['Username']],
                           body= f'{message}\n\n sent by :{name} \n Mobile: {phone} \n Sender email:{email}'  )

    img4= url_for('static', filename='assets/img/contact.png')
    return render_template('contact.html',image_url=img4, govind=govind)



@app.route("/edit/<string:Sno>", methods=['GET','POST'])
def edit(Sno):
    
    if ('user') in session and session['user']==govind['nameuser']:
        if(request.method=='POST'):
            title=request.form.get('Title')
            subheading=request.form.get('subheading')
            content=request.form.get('content')
            slug=request.form.get('slug')
            img_file=request.form.get('img')
            date=datetime.now()

            if Sno=='0':
                posted=Posts(title=title,subheading=subheading,content=content,slug=slug,img_file=img_file,date=date)
                db.session.add(posted)
                db.session.commit()
                return redirect('/admin')
            else:
                posted=Posts.query.filter_by(sNo=Sno).first()
                posted.title=title
                posted.subheading=subheading
                posted.content=content
                posted.slug=slug
                posted.img_file=img_file
                posted.date=date
                db.session.commit()
                return redirect('/edit/'+Sno)
                
        posted=Posts.query.filter_by(sNo=Sno).first()
        img4= url_for('static', filename='assets/img/edit.webp')
        return render_template('edit.html',govind=govind,Sno=Sno,posted=posted,img_url=img4)
    
    
@app.route("/delete/<string:Sno>")
def delete(Sno):
    if (('user') in session and session['user']==govind['nameuser']): 
        posted=Posts.query.filter_by(sNo=Sno).first()
        db.session.delete(posted)
        db.session.commit()
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True,port=8000)