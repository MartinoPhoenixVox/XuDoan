from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, BooleanField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Optional, URL

class RegistrationThieuNhiForm(FlaskForm):
    hoTen = StringField('Họ và tên', validators=[DataRequired(), Length(max=100)])
    ngaySinh = DateField('Ngày sinh (dd/MM/yyyy)', format='%d/%m/%Y', validators=[DataRequired()])
    giaoXu = StringField('Giáo xứ', validators=[DataRequired(), Length(max=100)])
    diaChi = StringField('Địa chỉ', validators=[DataRequired(), Length(max=255)])
    matKhau = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Đăng ký')

class RegistrationPhuHuynhForm(FlaskForm):
    hoTen = StringField('Họ và tên', validators=[DataRequired(), Length(max=100)])
    soDienThoai = StringField('Số điện thoại', validators=[
        DataRequired(),
        Regexp(r'^0\d{9,10}$', message="Số điện thoại không hợp lệ")
    ])
    matKhau = PasswordField('Mật khẩu', validators=[
        DataRequired(),
        Length(min=8, message="Mật khẩu phải có ít nhất 8 ký tự"),
        Regexp(r'(?=.*\d)(?=.*[A-Z])', message="Mật khẩu phải chứa ít nhất 1 số và 1 chữ hoa")
    ])
    submit = SubmitField('Đăng ký')

class LoginForm(FlaskForm):
    hoTen = StringField('Họ và tên', validators=[DataRequired()])
    matKhau = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

class ExcelUploadForm(FlaskForm):
    file = FileField('File Excel', validators=[Optional()])
    sheet_url = StringField('Link Google Sheets', validators=[Optional(), URL()])
    submit = SubmitField('Import')
