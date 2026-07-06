from flask import Blueprint, render_template
from flask_login import login_required

chat = Blueprint("chat", __name__)

@chat.route("/")
@login_required
def index():
    return render_template("chat.html")

from flask import jsonify
from flask_login import login_required
from models import Message

@chat.route("/history")
@login_required
def chat_history():
    messages = (
        Message.query
        .order_by(Message.timestamp.desc())  # ✅ 先取最新的120条（从新到旧）
        .limit(120)
        .all()
    )
    messages.reverse()

    data = []
    for m in messages:
        data.append({
            "username": m.user.username,
            "content": m.content,
            "timestamp": m.beijing_time_str
        })

    return jsonify(data)

from flask import render_template
from flask_login import login_required, current_user


@chat.route('/user/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template(
        'user_profile.html',
        user=user,
        current_user=current_user
    )


@chat.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user

    if request.method == 'POST':
        user.real_name = request.form.get('real_name')
        user.bio = request.form.get('bio')
        user.status = request.form.get('status')

        db.session.commit()
        return redirect(url_for('chat.user_profile', username=user.username))

    return render_template('edit_profile.html', user=user)