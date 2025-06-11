from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Notification, db

notification = Blueprint('notification', __name__)
# 通知ルート
@notification.route('/notifications')
@login_required
def notifications():
    notes = Notification.query.filter_by(user_id=current_user.id)\
            .order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notes)

# 差し戻しデータ削除処理
@notification.route('/notification/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    note = Notification.query.get_or_404(notification_id)
    if note.user_id != current_user.id:
        flash('この通知を削除する権限がありません。', 'danger')
        return redirect(url_for('notification.notifications'))

    db.session.delete(note)
    db.session.commit()
    flash('通知を削除しました。', 'success')

    return redirect(url_for('notification.notifications'))