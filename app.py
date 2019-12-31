from flask import Flask, render_template, url_for, request, redirect, flash,current_app
from flask_mysqldb import MySQL
import os
import secrets

app = Flask(__name__)
mysql = MySQL(app)



app.config['SECRET_KEY'] = 'fddddddddddd'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '11111'
app.config['MYSQL_DB'] = 'appsdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'





post=[
    {'id':1,
    'title': 'Hello Flask',
    'body':'ndustry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheet'
    
    },
     {'id':2,
    'title': 'Hello Flask 2',
    'body':'ndustry. Lorem Ipsum has been the industry type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s wi'
    
    },
     {'id':3,
    'title': 'Hello Flask',
    'body':'ndustry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheet'
    
    },
     {'id':4,
    'title': 'Hello Flask 2',
    'body':'ndustry. Lorem Ipsum has been the industry type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s wi'
    
    }
]

def save_images(photo):
     hash_photo = secrets.token_urlsafe(10)
     _, file_extention = os.path.splitext(photo.filename)
     photo_name = hash_photo + file_extention
     file_path = os.path.join(current_app.root_path, 'static/images', photo_name)
     photo.save(file_path)
     return photo_name


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM post ORDER By id DESC")
    blog = cur.fetchall()
    
    return render_template('index.html', post=blog)

@app.route('/single/<int:id>')    
def single(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM post WHERE id=%s", [id])
    blog=cur.fetchone()
    return render_template('single.html', post=blog)

@app.route('/dashboard')
def about():
    return render_template('about.html')

@app.route('/write', methods=['POST','GET'])
def write():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        img = save_images(request.files['img'])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO post(title, body, img)" "VALUES(%s,%s,%s)",(title, body,img))
        mysql.connection.commit()
        cur.close()
        flash('Your blog has been successfully inserted', 'success')
        return redirect('/')

    return render_template('write.html')  

@app.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        img = save_images(request.files['img'])

        cur = mysql.connection.cursor()
        cur.execute("UPDATE post SET title=%s, body=%s,img=%s WHERE id=%s",(title, body,img, id))
        mysql.connection.commit()
        cur.close()
        flash('Your blog has been successfully Updated', 'success')
        return redirect('/')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM post WHERE id=%s", [id])
    post = cur.fetchone()    

    return render_template('edit.html', post=post) 


@app.route('/delete/<int:id>')         
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM post WHERE id=%s",[id])
    mysql.connection.commit()
    flash("Your blog has been deleted", 'danger')
    return redirect(url_for('index'))
    

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return 'Logout Successfull'



if __name__=="__main__":
    app.run(debug=True)