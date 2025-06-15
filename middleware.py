from functools import wraps
from flask import session, redirect, flash, url_for, request

def login_required(roles=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            _roles = roles
            if 'user_id' not in session:
                flash("Vui lòng đăng nhập", "warning")
                return redirect(url_for('main.login'))

            user_type = session.get('user_type')
            if _roles and user_type not in roles:
                abort(403)

            # Kiểm tra PH chỉ truy cập TN của mình
            if user_type == 'phuhuynh' and request.endpoint in ['edit_thieu_nhi']:
                tn_id = kwargs.get('id')
                if not ThieuNhi_PhuHuynh.query.filter_by(idPhuHuynh=session['user_id'], idThieuNhi=tn_id).first():
                    abort(403)

            if _roles:
                if isinstance(roles, str):
                    _roles = [_roles]
                if session['user_type'] not in roles:
                    abort(403)
                    flash("Không có quyền truy cập", "danger")
                    return redirect(url_for('main.login'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
