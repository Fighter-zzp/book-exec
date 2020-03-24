from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/eshdemo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.secret_key = 'jklow'

'''
创建作者和书本模型
'''


class Author(db.Model):
    # 表名
    __tablename__ = 'authors'

    # 字段
    aid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # 关系引用
    # books是给自己(Author模型)用的, author是给Book模型用的
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author: %s' % self.name


# 书籍模型
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.aid'))

    def __repr__(self):
        return 'Book: %s %s' % (self.name, self.author_id)


# 自定义表单类
class AuthorForm(FlaskForm):
    author = StringField('作者', validators=[DataRequired()])
    book = StringField('书籍', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/', methods=['POST', 'GET'])
def index():
    author_form = AuthorForm()
    if author_form.validate_on_submit():
        author_name = author_form.author.data
        book_name = author_form.book.data
        author = Author.query.filter_by(name=author_name).first()

        if author:
            book = Book.query.filter_by(name=book_name).first()
            if book:
                flash('书名已存在')
            else:
                try:
                    new_book = Book(name=book_name, author_id=author.aid)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('书本添加失败')
                    db.session.rollback()

        else:
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()

                new_book = Book(name=book_name, author_id=new_author.aid)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('添加作者和书籍失败')
                db.session.rollback()

    else:
        if request.method == 'POST':
            flash('参数不全')
    authors = Author.query.all()

    return render_template('book.html', authors=authors, form=author_form)


@app.route('/delete_author/<int:aid>')
def delete_author(aid):
    author = Author.query.get(aid)
    if author:
        try:
            Book.query.filter_by(author_id=author.aid).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除作者出错')
            db.session.rollback()
    return redirect(url_for('index'))


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)

    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除书籍出错')
            db.session.rollback()

    else:
        flash('书籍找不到')

    return redirect(url_for('index'))


@app.route('/init')
def init():
    """
    初始化表格
    :return:
    """
    db.drop_all()
    db.create_all()

    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老惠')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.aid)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.aid)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.aid)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.aid)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.aid)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()
    return 'hi earth!'


if __name__ == '__main__':
    app.run()
