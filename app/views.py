from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Lread, User
from app.forms import LoginForm


@app.route('/')
def index():
    return redirect(url_for('main'))

@app.route('/main')
def main():
    myForm = LoginForm()
    novels = Lread.query.with_entities(Lread.id,Lread.title,Lread.art_title,Lread.auth).order_by(Lread.id.desc()).distinct().limit(20).all()
    return render_template('index.html', novels=novels,form=myForm)

@app.route('/login', methods=['POST','GET'])
def login():
    myForm = LoginForm(request.form)
    novels = Lread.query.with_entities(Lread.id,Lread.title,Lread.art_title,Lread.auth).order_by(Lread.id.desc()).distinct().limit(20).all()
    if request.method == "POST":
        user = User(myForm.username.data, myForm.password.data)
        if user.isExisted():
            # login_user(user)
            return render_template('index.html', novels=novels, user=user)
        else:
            return render_template('index.html', form=myForm,novels=novels)
    return render_template('index.html', form=myForm, novels=novels)

@app.route('/register', methods=['POST','GET'])
def register():
    myForm = LoginForm(request.form)
    if request.method == "POST":
        user = User(myForm.username.data, myForm.password.data)
        user.add()
        return redirect(url_for('main'))
    else:
        return render_template('register.html', form=myForm)

@app.route('/search', methods=['GET','POST'])
def search():
    myForm = LoginForm()
    if request.method == "POST":
        data = request.form.get('search')
        novels = Lread.query.filter_by(title=data).order_by(Lread.art_num).all()
        novels_text = Lread.query.filter_by(art_title=data).first()
        if novels:
            return render_template('index_detail.html', novels=novels, form=myForm)
        elif novels_text:
            return render_template('index_detail.html', text=novels_text, form=myForm)
        else:
            message = "你找的" + data + "不存在"
            return render_template('index_detail.html',message=message, form=myForm)
    else:
        novels = Lread.query.filter_by(title=request.args.get('q')).order_by(Lread.art_num).all()
        novels_type = Lread.query.with_entities(Lread.title, Lread.novel_type).filter_by(novel_type=request.args.get('q')).distinct().all()
        if novels:
            return render_template('index_detail.html', novels=novels, form=myForm)
        elif novels_type:
            return render_template('index_detail.html', novels_type=novels_type,form=myForm)
        else:
            novels_type = request.args.get('q')
            message = "你找的" + novels_type[:-2].strip('小说') + "小说或章节不存在"
            return render_template('index_detail.html',message=message, form=myForm)

@app.route('/read/<id>', methods=['GET',])
def read(id):
    myForm = LoginForm()
    text = Lread.query.filter_by(id=id).first()
    if text is None:
        message = "你找的小说或章节不存在"
        return render_template('index_detail.html',message=message, form=myForm)
    else:
        return render_template('index_detail.html',text = text, form=myForm)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404