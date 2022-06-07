# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request, session, redirect, url_for
from models.model import OnegaiContent, User
from models.database import db_session
from datetime import datetime
from models.key import key   #不要か、key.pyのSECRET_KEYか。
from hashlib import sha256
import os

# Flaskオブジェクトの生成
app = Flask(__name__)
app.secret_key = key.SECRET_KEY


@app.route("/")
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        all_onegai = OnegaiContent.query.all()
        return render_template("index.html", name=name, all_onegai=all_onegai)
    else:
        return redirect(url_for("top"))


@app.route("/add", methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = OnegaiContent(title, body, datetime.now())
    db_session.add(content)
    try:
        #db_session.query(content).update({'end': datetime.now()})  # 全データの'end'を更新
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()
    return redirect(url_for("index"))


@app.route("/update", methods=["post"])
def update():
    content = OnegaiContent.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.add(content)
    try:
        #db_session.query(content).update({'end': datetime.now()})  # 全データの'end'を更新
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()
    return redirect(url_for("index"))


@app.route("/delete", methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for ids in id_list:
        content = OnegaiContent.query.filter_by(id=ids).first()
        db_session.delete(content)
    try:
        #db_session.query(content).update({'end': datetime.now()})
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()
    return redirect(url_for("index"))


@app.route("/top")
def top():
    status = request.form.getlist("status")
    return render_template("top.html", status=status)


@app.route("/login", methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]     #ログインフォーム入力されたパスワードを代入
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()     #ログインフォームデータで生成したハッシュ値を代入
        H = User.query.filter_by(hashed_password=hashed_password).first()
        if H:     #ここが不都合だからelseにいく　ハッシュ値
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top", status="wrong_password"))
    else:
        return redirect(url_for("top", status="user_notfound"))


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html", status=status)


@app.route("/register", methods=["post"])
def register():
    user_name = request.form["user_name"]   #登録フォームからのユーザーネームデータを代入。
    user = User.query.filter_by(user_name=user_name).first()    #そのデータでフィルタリングしたDBの最初の値を代入
    if user:
        return redirect(url_for("newcomer", status="exist_user"))
    else:
        password = request.form["password"]     #登録フォームからパスワードデータを代入
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        try:
            #db_session.query(user).update({'end': datetime.now()})  # 全データの'end'を更新
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()
        session["user_name"] = user_name    #これは何？　セッションによる閲覧制御とsessionとは配列なのか、　= user_nameはformで入力された値。
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top", status="logout"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
