from flask_sqlalchemy import SQLAlchemy
from extensions import db
from datetime import date, datetime
import re
import random
from sqlalchemy.dialects.mysql import TIMESTAMP

class ThieuNhi(db.Model):
    __tablename__ = 'ThieuNhi'
    idThieuNhi = db.Column(db.String(12), primary_key=True)
    tenThanh = db.Column(db.String(50))
    hoTen = db.Column(db.String(100), nullable=False)
    ngaySinh = db.Column(db.Date, nullable=False)
    giaoXu = db.Column(db.String(100), nullable=False)
    ngayRuaToi = db.Column(db.Date)
    ngayRuocLe = db.Column(db.Date)
    ngayThemSuc = db.Column(db.Date)
    diaChi = db.Column(db.String(255), nullable=False)
    matKhau = db.Column(db.String(60))
    ghiChu = db.Column(db.Text)

    phuhuynhs = db.relationship('PhuHuynh', secondary='ThieuNhi_PhuHuynh')
    phandoans = db.relationship('PhanDoan', secondary='PhanDoan_ThieuNhi')
    diemdanhs = db.relationship('DiemDanh', backref='thieunhi')

    @staticmethod
    def generate_id(hoTen, ngaySinh):
        replacements = {
          'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
          'Đ': 'D',
          'É': 'E', 'È': 'E', 'Ê': 'E',
          'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Ơ': 'O',
          'Ã': 'A', 'À': 'A', 'Á': 'A', 'Ạ': 'A',
          'Ý': 'Y', 'Ỳ': 'Y', 'Ỵ': 'Y',
          'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ư': 'U',
          'Í': 'I', 'Ì': 'I', 'Ị': 'I',
          'Ạ': 'A', 'Ả': 'A', 'Ã': 'A', 'Â': 'A',
          'Ê': 'E', 'Ế': 'E', 'Ề': 'E', 'Ệ': 'E',
          'Ô': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ộ': 'O',
          'Ư': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ự': 'U',
          'Đ': 'D', 'Ỏ': 'O', 'Ỡ': 'O', 'Ợ': 'O',
          'Ỳ': 'Y', 'Ỵ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y'
        }
        pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))
        hoTen = pattern.sub(lambda m: replacements[m.group(0)], hoTen.upper())
        parts = re.split(r'[ .,-]+', hoTen.strip(' .,-'))
        code = parts[0][0] + parts[-1][0]
        return f"TN{code.upper()}{ngaySinh.strftime('%d%m%Y')}"

class PhuHuynh(db.Model):
    __tablename__ = 'PhuHuynh'
    idPhuHuynh = db.Column(db.String(13), primary_key=True)
    tenThanh = db.Column(db.String(50))
    hoTen = db.Column(db.String(100), nullable=False)
    soDienThoai = db.Column(db.String(20), nullable=False)
    matKhau = db.Column(db.String(60))

    thieunhis = db.relationship('ThieuNhi', secondary='ThieuNhi_PhuHuynh')

    @staticmethod
    def generate_id(hoTen, soDienThoai):
        replacements = {
          'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
          'Đ': 'D',
          'É': 'E', 'È': 'E', 'Ê': 'E',
          'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Ơ': 'O',
          'Ã': 'A', 'À': 'A', 'Á': 'A', 'Ạ': 'A',
          'Ý': 'Y', 'Ỳ': 'Y', 'Ỵ': 'Y',
          'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ư': 'U',
          'Í': 'I', 'Ì': 'I', 'Ị': 'I',
          'Ạ': 'A', 'Ả': 'A', 'Ã': 'A', 'Â': 'A',
          'Ê': 'E', 'Ế': 'E', 'Ề': 'E', 'Ệ': 'E',
          'Ô': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ộ': 'O',
          'Ư': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ự': 'U',
          'Đ': 'D', 'Ỏ': 'O', 'Ỡ': 'O', 'Ợ': 'O',
          'Ỳ': 'Y', 'Ỵ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y'
        }
        pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))
        hoTen = pattern.sub(lambda m: replacements[m.group(0)], hoTen.upper())
        parts = re.split(r'[ .,-]+', hoTen.strip(' .,-'))
        code = parts[-1][0]
        return f"PH{code.upper()}{soDienThoai}"

class ThieuNhi_PhuHuynh(db.Model):
    __tablename__ = 'ThieuNhi_PhuHuynh'
    idThieuNhi = db.Column(db.String(12), db.ForeignKey('ThieuNhi.idThieuNhi'), primary_key=True)
    idPhuHuynh = db.Column(db.String(13), db.ForeignKey('PhuHuynh.idPhuHuynh'), primary_key=True)
    vaiTro = db.Column(db.Enum('Cha','Mẹ','Người giám hộ'), nullable=False)

class PhanDoan(db.Model):
    __tablename__ = 'PhanDoan'
    idPhanDoan = db.Column(db.String(10), primary_key=True)
    tenPhanDoan = db.Column(db.String(100), nullable=False)
    namHoc = db.Column(db.String(20), nullable=False)
    nganh = db.Column(db.Enum('Chiên Con','Ấu Nhi','Thiếu Nhi','Nghĩa Sĩ','Hiệp Sĩ'))

    @staticmethod
    def generate_id(tenPhanDoan, namHoc):
        parts_1 = tenPhanDoan.strip().split()
        parts_2 = namHoc.strip().split('-')
        if parts_1[0][0] == 'Ấ':
          code_1 = parts_1[0][0].replace('Ấ', 'A') + parts_1[-2][0] + parts_1[-1][0]
        else:
          code_1 = parts_1[0][0] + parts_1[-2][0] + parts_1[-1][0]
        code_2 = parts_2[0][1:] + parts_2[1][1:]
        return f"{code_1}" + "-" + f"{code_2}"

class PhanDoan_ThieuNhi(db.Model):
    __tablename__ = 'PhanDoan_ThieuNhi'
    idPhanDoan = db.Column(db.String(10), db.ForeignKey('PhanDoan.idPhanDoan'), primary_key=True)
    idThieuNhi = db.Column(db.String(12), db.ForeignKey('ThieuNhi.idThieuNhi'), primary_key=True)
    hocKy = db.Column(db.Integer, primary_key=True)
    diemKiemTra1 = db.Column(db.Float)
    diemKiemTra2 = db.Column(db.Float)
    diemKiemTra3 = db.Column(db.Float)
    diemThi = db.Column(db.Float)
    diemTrungBinh = db.Column(db.Float)
    hocLuc = db.Column(db.Enum('Xuất sắc','Giỏi','Khá','Trung bình','Yếu'))
    hanhKiem = db.Column(db.Enum('Đạt','Không đạt'))

class DiemDanh(db.Model):
    __tablename__ = 'DiemDanh'
    idThieuNhi = db.Column(db.String(12), db.ForeignKey('ThieuNhi.idThieuNhi'), primary_key=True)
    idPhanDoan = db.Column(db.String(10), db.ForeignKey('PhanDoan.idPhanDoan'), primary_key=True)
    ngayDiemDanh = db.Column(db.Date, primary_key=True)
    thoiGianDiemDanh = db.Column(db.TIMESTAMP)
    coMatThanhLe = db.Column(db.Boolean)
    diTreThanhLe = db.Column(db.Boolean)
    coMatGiaoLy = db.Column(db.Boolean)
    vangPhep = db.Column(db.Boolean)

    phan_doan = db.relationship('PhanDoan', backref='diem_danh')

class NhanSu(db.Model):
    __tablename__ = 'NhanSu'
    idNhanSu = db.Column(db.String(10), primary_key=True)
    tenThanh = db.Column(db.String(50), nullable=False)
    hoTen = db.Column(db.String(100), nullable=False)
    chucDanh = db.Column(db.Enum('Linh mục','Tu sĩ','Nữ tu'))
    hoiDong = db.Column(db.String(100))
    ngaySinh = db.Column(db.Date)
    giaoXu = db.Column(db.String(100))
    soDienThoai = db.Column(db.String(20))
    email = db.Column(db.String(100))
    diaChi = db.Column(db.String(255))
    dangHoatDong = db.Column(db.Boolean, nullable=False)
    matKhau = db.Column(db.String(60))

    @staticmethod
    def generate_id(hoTen, ngaySinh, tenThanh):
        replacements = {
          'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
          'Đ': 'D',
          'É': 'E', 'È': 'E', 'Ê': 'E',
          'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Ơ': 'O',
          'Ã': 'A', 'À': 'A', 'Á': 'A', 'Ạ': 'A',
          'Ý': 'Y', 'Ỳ': 'Y', 'Ỵ': 'Y',
          'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ư': 'U',
          'Í': 'I', 'Ì': 'I', 'Ị': 'I',
          'Ạ': 'A', 'Ả': 'A', 'Ã': 'A', 'Â': 'A',
          'Ê': 'E', 'Ế': 'E', 'Ề': 'E', 'Ệ': 'E',
          'Ô': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ộ': 'O',
          'Ư': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ự': 'U',
          'Đ': 'D', 'Ỏ': 'O', 'Ỡ': 'O', 'Ợ': 'O',
          'Ỳ': 'Y', 'Ỵ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y'
        }
        pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))
        tenThanh = pattern.sub(lambda m: replacements[m.group(0)], tenThanh.upper())
        random.seed(tenThanh)
        parts = hoTen.strip().split()
        code = parts[0][0] + parts[-1][0]
        parts_2 = list(re.split(r'[ .,-]+', tenThanh.strip(' .,-')))
        code_2 = ""
        for i in range(len(tenThanh)):
          if i == 6:
            break
          else:
            code_2 = code_2 + random.choice(tenThanh)
        if ngaySinh != None:
          return f"NS{code.upper()}{ngaySinh.strftime('%d%m%y')}"
        else:
          return f"NS{code.upper()}{code_2.upper()}"

class PhanDoan_NhanSu(db.Model):
    __tablename__ = 'PhanDoan_NhanSu'
    idPhanDoan = db.Column(db.String(10), db.ForeignKey('PhanDoan.idPhanDoan'), primary_key=True)
    idNhanSu = db.Column(db.String(10), db.ForeignKey('NhanSu.idNhanSu'), primary_key=True)
    vaiTro = db.Column(db.Enum('Phân Đoàn Trưởng','Phân Đoàn Phó','Huấn Giáo','Huynh Trưởng','Dự Trưởng'))

class PhanDoan_TroTa(db.Model):
    __tablename__ = 'PhanDoan_TroTa'
    idPhanDoan = db.Column(db.String(10), db.ForeignKey('PhanDoan.idPhanDoan'), primary_key=True)
    idTroTa = db.Column(db.String(13), db.ForeignKey('PhuHuynh.idPhuHuynh'), primary_key=True)

class EditRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    field = db.Column(db.String(50), nullable=False)
    new_value = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.now)
