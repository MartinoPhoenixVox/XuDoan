from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify, send_file
from extensions import db, bcrypt
from models import ThieuNhi, PhuHuynh, NhanSu, DiemDanh, PhanDoan, ThieuNhi_PhuHuynh
from forms import RegistrationThieuNhiForm, RegistrationPhuHuynhForm, LoginForm, ExcelUploadForm
from utils import generate_qr_code, parse_excel_sheet
from datetime import datetime, date
from middleware import login_required
import pandas as pd
from io import BytesIO
import gspread
from google_sheets import get_google_sheet
from sqlalchemy.orm import joinedload

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = ThieuNhi.query.filter_by(hoTen=form.hoTen.data).first()
        if user and bcrypt.check_password_hash(user.matKhau, form.matKhau.data):
            session['user_type'] = 'thieunhi'
            session['user_id'] = user.idThieuNhi
            return redirect(url_for('main.dashboard_thieunhi'))
        user = PhuHuynh.query.filter_by(hoTen=form.hoTen.data).first()
        if user and bcrypt.check_password_hash(user.matKhau, form.matKhau.data):
            session['user_type'] = 'phuhuynh'
            session['user_id'] = user.idPhuHuynh
            return redirect(url_for('main.dashboard_phuhuynh'))
        user = NhanSu.query.filter_by(hoTen=form.hoTen.data).first()
        if user and bcrypt.check_password_hash(user.matKhau, form.matKhau.data):
            if not user.dangHoatDong:
                flash("Tài khoản đã bị vô hiệu hóa", "danger")
                return redirect(url_for('main.login'))
            else:
                session['user_type'] = 'nhansu'
                session['user_id'] = user.idNhanSu
                return redirect(url_for('main.dashboard_nhansu'))
        flash('Đăng nhập thất bại hoặc không có quyền truy cập.', 'danger')
    return render_template('login.html', form=form)

@main.route('/register/thieunhi', methods=['GET', 'POST'])
def register_thieunhi():
    form = RegistrationThieuNhiForm()
    if form.validate_on_submit():
        exists = ThieuNhi.query.filter_by(hoTen=form.hoTen.data, ngaySinh=form.ngaySinh.data).first()
        if exists:
            flash('Thiếu nhi đã tồn tại.', 'danger')
            return render_template('register_thieunhi.html', form=form)
        id_tn = ThieuNhi.generate_id(form.hoTen.data, form.ngaySinh.data)
        pw_hash = bcrypt.generate_password_hash(form.matKhau.data).decode('utf-8')
        tn = ThieuNhi(idThieuNhi=id_tn, hoTen=form.hoTen.data, ngaySinh=form.ngaySinh.data,
                      giaoXu=form.giaoXu.data, diaChi=form.diaChi.data, matKhau=pw_hash)
        db.session.add(tn)
        db.session.commit()
        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('login'))
    return render_template('register_thieunhi.html', form=form)

@main.route('/register/phuhuynh', methods=['GET', 'POST'])
def register_phuhuynh():
    form = RegistrationPhuHuynhForm()
    if form.validate_on_submit():
        exists = PhuHuynh.query.filter_by(hoTen=form.hoTen.data, soDienThoai=form.soDienThoai.data).first()
        if exists:
            flash('Phụ huynh đã tồn tại.', 'danger')
            return render_template('register_phuhuynh.html', form=form)
        id_ph = PhuHuynh.generate_id(form.hoTen.data, form.soDienThoai.data)
        pw_hash = bcrypt.generate_password_hash(form.matKhau.data).decode('utf-8')
        ph = PhuHuynh(idPhuHuynh=id_ph, hoTen=form.hoTen.data,
                      soDienThoai=form.soDienThoai.data, matKhau=pw_hash)
        db.session.add(ph)
        db.session.commit()
        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('login'))
    return render_template('register_phuhuynh.html', form=form)

@main.route('/logout')
def logout():
    session.clear()
    flash("Đăng xuất thành công.", "info")
    return redirect(url_for('main.login'))

@main.route('/scan_qr', methods=['POST'])
def scan_qr():
    data = request.json
    idTN = data.get('idThieuNhi')
    idPD = data.get('idPhanDoan')
    today = date.today()
    dd = DiemDanh(idThieuNhi=idTN, idPhanDoan=idPD, ngayDiemDanh=today,
                  thoiGianDiemDanh=datetime.now(), coMatThanhLe=True)
    db.session.merge(dd)
    db.session.commit()
    # Thêm logic cập nhật lên Google Sheets
    if not ThieuNhi.query.get(idTN) or not PhanDoan.query.get(idPD):
        return jsonify({'status': 'error', 'message': 'Dữ liệu không hợp lệ'}), 400
    try:
        sheet = get_google_sheet(os.getenv('ATTENDANCE_SHEET_URL'))
        sheet.append_row([
            idTN,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Có mặt'
        ])
    except Exception as e:
        print("Lỗi cập nhật Google Sheet:", str(e))
    return jsonify({'status': 'ok', 'message': 'Điểm danh thành công'})

@main.route('/dashboard/thieunhi')
@login_required(roles='thieunhi')
def dashboard_thieunhi():
    user = ThieuNhi.query.options(
        joinedload(ThieuNhi.diemdanhs).joinedload(DiemDanh.phan_doan)
    ).get(session['user_id'])
    return render_template('dashboard_thieunhi.html', user=user)

@main.route('/dashboard/phuhuynh')
@login_required(roles='phuhuynh')
def dashboard_phuhuynh():
    user = PhuHuynh.query.get(session['user_id'])
    return render_template('dashboard_phuhuynh.html', user=user)

@main.route('/dashboard/nhansu')
@login_required(roles='nhansu')
def dashboard_nhansu():
    user = NhanSu.query.get(session['user_id'])
    # Kiểm tra vai trò người dùng (giả sử NhanSu)
    if user.__class__.__name__ != 'NhanSu' or not user.dangHoatDong:
        return render_template('error.html', message="Bạn không có quyền truy cập trang này"), 403

    # Lấy dữ liệu thống kê
    total_thieu_nhi = db.session.query(ThieuNhi).count()
    total_phu_huynh = db.session.query(PhuHuynh).count()
    total_phan_doan = db.session.query(PhanDoan).filter(PhanDoan.namHoc == '2024-2025').count()

    # Lấy danh sách Thiếu Nhi
    thieu_nhi_list = db.session.query(ThieuNhi).all()

    # Lấy danh sách Phụ Huynh và Thiếu Nhi liên quan
    phu_huynh_list = db.session.query(PhuHuynh, ThieuNhi.hoTen.label('thieu_nhi_quan_ly'))\
        .outerjoin(ThieuNhi_PhuHuynh, PhuHuynh.idPhuHuynh == ThieuNhi_PhuHuynh.idPhuHuynh)\
        .outerjoin(ThieuNhi, ThieuNhi_PhuHuynh.idThieuNhi == ThieuNhi.idThieuNhi)\
        .all()

    # Tạo danh sách Phụ Huynh với thông tin Thiếu Nhi quản lý
    phu_huynh_data = {}
    for phu_huynh, thieu_nhi_name in phu_huynh_list:
        if phu_huynh.idPhuHuynh not in phu_huynh_data:
            phu_huynh_data[phu_huynh.idPhuHuynh] = {
                'hoTen': phu_huynh.hoTen,
                'soDienThoai': phu_huynh.soDienThoai,
                'thieu_nhi_quan_ly': []
            }
        if thieu_nhi_name:
            phu_huynh_data[phu_huynh.idPhuHuynh]['thieu_nhi_quan_ly'].append(thieu_nhi_name)


    return render_template(
        'dashboard_nhansu.html',
        user=user,
        stats={
            'total_thieu_nhi': total_thieu_nhi,
            'total_phu_huynh': total_phu_huynh,
            'total_phan_doan': total_phan_doan
        },
        thieu_nhi_list=thieu_nhi_list,
        phu_huynh_list=list(phu_huynh_data.values())
    )

@main.route('/manage_phandoan', methods=['GET', 'POST'])
@login_required(roles='nhansu')
def manage_phandoan():
    if request.method == 'POST':
        ten = request.form['tenPhanDoan']
        nam_hoc = request.form['namHoc']
        nganh = request.form['nganh']
        pd = PhanDoan(
            idPhanDoan=PhanDoan.generate_id(ten, nam_hoc),
            tenPhanDoan=ten,
            namHoc=nam_hoc,
            nganh=nganh
        )
        db.session.add(pd)
        db.session.commit()
        flash('Tạo phân đoàn thành công', 'success')
        return redirect(url_for('main.manage_phandoan'))

    phandoans = PhanDoan.query.all()
    return render_template('manage_phandoan.html', phandoans=phandoans)

@main.route('/delete_phandoan/<id>', methods=['POST'])
@login_required(roles='nhansu')
def delete_phandoan(id):
    phandoan = PhanDoan.query.get_or_404(id)
    try:
        db.session.delete(phandoan)
        db.session.commit()
        flash('Đã xóa phân đoàn thành công', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi xóa phân đoàn: {str(e)}', 'danger')
    return redirect(url_for('main.manage_phandoan'))

@main.route('/request-edit', methods=['POST'])
@login_required(roles=['phuhuynh', 'thieunhi'])
def request_edit():
    data = request.get_json()
    user_type = session['user_type']
    id_thieu_nhi = data.get('idThieuNhi')

    # Tạo yêu cầu chỉnh sửa
    edit_request = {
        'user_id': session['user_id'],
        'user_type': user_type,
        'field': data['field'],
        'new_value': data['new_value'],
        'status': 'pending',
        'timestamp': datetime.now().isoformat()
    }

    # Lưu vào database (cần thêm model EditRequest)
    new_request = EditRequest(
        user_id=edit_request['user_id'],
        user_type=edit_request['user_type'],
        idThieuNhi=id_thieu_nhi,
        field=edit_request['field'],
        new_value=edit_request['new_value'],
        status=edit_request['status']
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Yêu cầu đã được gửi đến quản trị viên'
    })

# Thêm route quản lý yêu cầu chỉnh sửa
@main.route('/manage-requests')
@login_required(roles='nhansu')
def manage_requests():
    requests = EditRequest.query.filter_by(status='pending').all()
    return render_template('manage_requests.html', requests=requests)

@main.route('/approve-request/<int:request_id>')
@login_required(roles='nhansu')
def approve_request(request_id):
    req = EditRequest.query.get_or_404(request_id)
    # Cập nhật dữ liệu theo req.field và req.new_value
    req = EditRequest.query.get_or_404(request_id)
    if req.user_type == 'phuhuynh' and req.idThieuNhi:
        tn = ThieuNhi.query.get(req.idThieuNhi)
    else:
        tn = ThieuNhi.query.get(req.user_id)
    setattr(tn, req.field, req.new_value)
    req.status = 'approved'
    db.session.commit()
    return redirect(url_for('main.manage_requests'))

@main.route('/reject-request/<int:request_id>')
@login_required(roles='nhansu')
def reject_request(request_id):
    req = EditRequest.query.get_or_404(request_id)
    req.status = 'rejected'
    db.session.commit()
    return redirect(url_for('main.manage_requests'))

@main.route('/import', methods=['GET', 'POST'])
@login_required(roles='nhansu')
def import_data():
    form = ExcelUploadForm()
    if form.validate_on_submit():
        try:
            df = parse_excel_sheet(file_stream=form.file.data, sheet_url=form.sheet_url.data)
            error_rows = []

            for idx, row in df.iterrows():
                try:
                    # Xử lý Thiếu Nhi
                    tn = ThieuNhi(
                        idThieuNhi=ThieuNhi.generate_id(row['HỌ_TÊN'], row['NGÀY_SINH']),
                        tenThanh=row['TÊN_THÁNH'],
                        hoTen=row['HỌ_TÊN'],
                        ngaySinh=datetime.strptime(row['NGÀY_SINH'], '%d/%m/%Y').date(),
                        giaoXu=row['GIÁO_XỨ'],
                        ngayRuaToi=row['RỬA_TỘI'],
                        ngayRuocLe=row['RƯỚC_LỄ'],
                        ngayThemSuc=row['THÊM_SỨC'],
                        diaChi=row['ĐỊA_CHỈ'],
                        ghiChu=row['GHI_CHÚ'],
                        matKhau=bcrypt.generate_password_hash('1234').decode('utf-8') # Mật khẩu mặc định
                    )
                    db.session.merge(tn)

                    # Xử lý Phụ Huynh (Cha)
                    if pd.notna(row['TÊN_CHA']):
                        ph_cha = PhuHuynh(
                            idPhuHuynh=PhuHuynh.generate_id(row['TÊN_CHA'], row['SĐT_CHA']),
                            hoTen=row['TÊN_CHA'],
                            soDienThoai=row['SĐT_CHA'].replace('.', ''),
                            matKhau=bcrypt.generate_password_hash('1234').decode('utf-8')
                        )
                        db.session.merge(ph_cha)
                        db.session.add(ThieuNhi_PhuHuynh(
                            idThieuNhi=ThieuNhi.generate_id(row['HỌ_TÊN'], row['NGÀY_SINH']),
                            idPhuHuynh=ph_cha.idPhuHuynh,
                            vaiTro='Cha'
                        ))

                    # Xử lý Phụ Huynh (Mẹ)
                    if pd.notna(row['TÊN_MẸ']):
                        ph_me = PhuHuynh(
                            idPhuHuynh=PhuHuynh.generate_id(row['TÊN_MẸ'], row['SĐT_MẸ']),
                            hoTen=row['TÊN_MẸ'],
                            soDienThoai=row['SĐT_MẸ'].replace('.', ''),
                            matKhau=bcrypt.generate_password_hash('1234').decode('utf-8')
                        )
                        db.session.merge(ph_me)
                        db.session.add(ThieuNhi_PhuHuynh(
                            idThieuNhi=ThieuNhi.generate_id(row['HỌ_TÊN'], row['NGÀY_SINH']),
                            idPhuHuynh=ph_me.idPhuHuynh,
                            vaiTro='Mẹ'
                        ))

                    # Xử lý Phụ Huynh (Người giám hộ)
                    if pd.notna(row['TÊN_GH']):
                        ph_gh = PhuHuynh(
                            idPhuHuynh=PhuHuynh.generate_id(row['TÊN_GH'], row['SĐT_GH']),
                            hoTen=row['TÊN_GH'],
                            soDienThoai=row['SĐT_GH'].replace('.', ''),
                            matKhau=bcrypt.generate_password_hash('1234').decode('utf-8')
                        )
                        db.session.merge(ph_me)
                        db.session.add(ThieuNhi_PhuHuynh(
                            idThieuNhi=ThieuNhi.generate_id(row['HỌ_TÊN'], row['NGÀY_SINH']),
                            idPhuHuynh=ph_gh.idPhuHuynh,
                            vaiTro='Người giám hộ'
                        ))

                except Exception as e:
                    error_rows.append({
                        'row': idx+4, # Vì bỏ qua 3 dòng đầu
                        'error': str(e),
                        'data': row.to_dict()
                    })

            if error_rows:
                flash(f'Import thành công với {len(df)-len(error_rows)} bản ghi. Lỗi ở {len(error_rows)} dòng', 'warning')
                session['import_errors'] = error_rows
            else:
                flash('Import thành công!', 'success')

            db.session.commit()
            return redirect(url_for('main.import_results'))

        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi hệ thống: {str(e)}', 'danger')
            # Ghi log lỗi chi tiết
            import traceback
            traceback.print_exc()

    return render_template('import.html', form=form)

@main.route('/import-results')
@login_required(roles='nhansu')
def import_results():
    errors = session.get('import_errors', [])
    return render_template('import_results.html', errors=errors)

# Route chỉnh sửa Thiếu Nhi
@main.route('/edit_thieu_nhi/<id>', methods=['GET', 'POST'])
@login_required(roles='nhansu')
def edit_thieu_nhi(id):
    thieu_nhi = ThieuNhi.query.get_or_404(id)
    if request.method == 'POST':
        thieu_nhi.hoTen = request.form['hoTen']
        thieu_nhi.ngaySinh = datetime.strptime(request.form['ngaySinh'], '%Y-%m-%d').date()
        thieu_nhi.giaoXu = request.form['giaoXu']
        thieu_nhi.diaChi = request.form['diaChi']
        thieu_nhi.tenThanh = request.form.get('tenThanh', '')
        try:
            db.session.commit()
            return redirect(url_for('main.dashboard_nhansu'))
        except Exception as e:
            db.session.rollback()
            return render_template('error.html', message=f"Lỗi khi cập nhật: {str(e)}"), 500
    return render_template('edit_thieu_nhi.html', thieu_nhi=thieu_nhi)

@main.route('/export-template')
@login_required(roles='nhansu')
def export_template():
    # Lấy dữ liệu từ CSDL
    thieu_nhi = ThieuNhi.query.all()

    # Tạo DataFrame
    data = []
    for tn in thieu_nhi:
        phuhuynh = PhuHuynh.query.join(ThieuNhi_PhuHuynh).filter(
            ThieuNhi_PhuHuynh.idThieuNhi == tn.idThieuNhi
        ).all()

        cha = next((ph for ph in phuhuynh if ph.vaiTro == 'Cha'), None)
        me = next((ph for ph in phuhuynh if ph.vaiTro == 'Mẹ'), None)
        gh = next((ph for ph in phuhuynh if ph.vaiTro == 'Người giám hộ'), None)

        data.append({
            'code': tn.idThieuNhi,
            'TÊN_THÁNH': tn.tenThanh,
            'HỌ_TÊN': tn.hoTen,
            'NGÀY_SINH': tn.ngaySinh,
            'GIÁO_XỨ': tn.giaoXu,
            'RỬA_TỘI': tn.ngayRuaToi,
            'RƯỚC_LỄ': tn.ngayRuocLe,
            'THÊM_SỨC': tn.ngayThemSuc,
            'ĐỊA_CHỈ': tn.diaChi,
            'TÊN_CHA': cha.hoTen if cha else '',
            'SĐT_CHA': cha.soDienThoai if cha else '',
            'TÊN_MẸ': me.hoTen if me else '',
            'SĐT_MẸ': me.soDienThoai if me else '',
            'TÊN_GH': gh.hoTen if me else '',
            'SĐT_GH': gh.soDienThoai if me else '',
        })

    df = pd.DataFrame(data)

    # Xuất file Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='THÔNG TIN', index=False)
    writer.close()
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        download_name='THONG_TIN_THIEU_NHI.xlsx',
        as_attachment=True
    )

# Route xóa Thiếu Nhi
@main.route('/delete_thieu_nhi/<id>', methods=['DELETE'])
@login_required(roles='nhansu')
def delete_thieu_nhi(id):
    thieu_nhi = ThieuNhi.query.get_or_404(id)
    try:
        db.session.delete(thieu_nhi)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Route chỉnh sửa Phụ Huynh
@main.route('/edit_phu_huynh/<id>', methods=['GET', 'POST'])
@login_required(roles='nhansu')
def edit_phu_huynh(id):
    phu_huynh = PhuHuynh.query.get_or_404(id)
    if request.method == 'POST':
        phu_huynh.hoTen = request.form['hoTen']
        phu_huynh.soDienThoai = request.form['soDienThoai']
        phu_huynh.tenThanh = request.form.get('tenThanh', '')
        try:
            db.session.commit()
            return redirect(url_for('main.dashboard_nhansu'))
        except Exception as e:
            db.session.rollback()
            return render_template('error.html', message=f"Lỗi khi cập nhật: {str(e)}"), 500
    return render_template('edit_phu_huynh.html', phu_huynh=phu_huynh)

# Route xóa Phụ Huynh
@main.route('/delete_phu_huynh/<id>', methods=['DELETE'])
@login_required(roles='nhansu')
def delete_phu_huynh(id):
    phu_huynh = PhuHuynh.query.get_or_404(id)
    try:
        db.session.delete(phu_huynh)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main.context_processor
def inject_year():
    from datetime import datetime
    return {'current_year': datetime.now().year}

@main.route('/api/charts-data')
@login_required
def charts_data():
    year = request.args.get('year', '2024')
    semester = request.args.get('semester', 'all')

    # Lấy dữ liệu từ database
    data = {
        'comparison': get_score_comparison(year, semester),
        'distribution': get_members_distribution(year),
        'progress': get_score_progress(year),
        'attendance': get_attendance_rate(year)
    }

    return jsonify(data)

@main.route('/charts', methods=['GET'])
@login_required(roles='nhansu')
def charts():
    return render_template('charts.html')

def get_score_comparison(year, semester):
    # Lấy điểm trung bình của các phân đoàn trong năm và học kỳ
    query = db.session.query(PhanDoan.tenPhanDoan, db.func.avg(PhanDoan_ThieuNhi.diemTrungBinh))\
        .join(PhanDoan_ThieuNhi)\
        .filter(PhanDoan.namHoc == year)
    if semester != 'all':
        query = query.filter(PhanDoan_ThieuNhi.hocKy == int(semester))
    result = query.group_by(PhanDoan.tenPhanDoan).all()

    return {
        'labels': [row[0] for row in result],
        'values': [float(row[1]) if row[1] else 0 for row in result]
    }

def get_members_distribution(year):
    # Đếm số Thiếu Nhi theo ngành trong năm
    result = db.session.query(PhanDoan.nganh, db.func.count(PhanDoan_ThieuNhi.idThieuNhi))\
        .join(PhanDoan_ThieuNhi)\
        .filter(PhanDoan.namHoc == year)\
        .group_by(PhanDoan.nganh).all()

    return {
        'labels': [row[0] for row in result],
        'counts': [row[1] for row in result],
        'colors': ['#4e73df', '#1cc88a', '#f6c23e', '#e74a3b'][:len(result)]
    }

def get_score_progress(year):
    # Lấy tiến độ điểm của các phân đoàn qua các học kỳ
    result = db.session.query(PhanDoan.tenPhanDoan, PhanDoan_ThieuNhi.hocKy, db.func.avg(PhanDoan_ThieuNhi.diemTrungBinh))\
        .join(PhanDoan_ThieuNhi)\
        .filter(PhanDoan.namHoc == year)\
        .group_by(PhanDoan.tenPhanDoan, PhanDoan_ThieuNhi.hocKy).all()

    labels = sorted(set(f'HK{row[1]} {year}' for row in result))
    datasets = {}
    for row in result:
        pd_name = row[0]
        label = f'HK{row[1]} {year}'
        if pd_name not in datasets:
            datasets[pd_name] = {'label': pd_name, 'data': [0] * len(labels), 'borderColor': '#4e73df'}
        idx = labels.index(label)
        datasets[pd_name]['data'][idx] = float(row[2]) if row[2] else 0

    return {
        'labels': labels,
        'datasets': list(datasets.values())
    }

def get_attendance_rate(year):
    # Tính tỷ lệ điểm danh chi tiết
    total = db.session.query(DiemDanh).filter(
        db.extract('year', DiemDanh.ngayDiemDanh) == year
    ).count()

    present = db.session.query(DiemDanh).filter(
        db.extract('year', DiemDanh.ngayDiemDanh) == year,
        DiemDanh.coMatThanhLe == True
    ).count()

    late = db.session.query(DiemDanh).filter(
        db.extract('year', DiemDanh.ngayDiemDanh) == year,
        DiemDanh.diTreThanhLe == True
    ).count()

    return {
        'present': present,
        'late': late,
        'absent': total - present - late,
        'total': total
    }
