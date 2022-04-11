from flask import Flask,  render_template
from threading import Thread

web = Flask('')
@web.route('/')

def home():
  return render_template('home.html')

@web.route('/home/')
def backhome():
    return render_template('home.html')
  
@web.route('/contact/')
def contact():
    return render_template('contact.html')

@web.route('/about/')
def about():
    return render_template('about.html')

@web.route('/oldabout/')
def oldabout():
    return render_template('oldabout.html')

@web.route('/oldhome/')
def oldhome():
    return render_template('oldhome.html')

@web.route('/oldcontact/')
def oldcontact():
    return render_template('oldcontact.html')
  
def run():
  web.run(host='0.0.0.0',port=8080)


def keep_alive():
   run_thread = Thread(target=run)
   run_thread.start()