from flask import render_template
import plotly.express as px
import pandas as pd
from models import PhanDoan, PhanDoan_ThieuNhi

@app.route('/nhansu/visualization', methods=['GET', 'POST'])
@login_required(roles='nhansu')
def nhansu_visualization():
    if current_user.user_type != 'nhan_su':
        return redirect('/')

    nam_hoc = request.form.get('nam_hoc', '2024-2025')
    phan_doans = PhanDoan.query.filter_by(namHoc=nam_hoc).all()
    data = []
    for pd in phan_doans:
        count = PhanDoan_ThieuNhi.query.filter_by(idPhanDoan=pd.idPhanDoan).count()
        data.append({'PhanDoan': pd.tenPhanDoan, 'SoLuong': count})

    df = pd.DataFrame(data)
    fig = px.bar(df, x='PhanDoan', y='SoLuong', title=f'Số lượng Thiếu Nhi theo Phân Đoàn ({nam_hoc})')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('nhansu_visualization.html', graphJSON=graphJSON)
