import qrcode
from io import BytesIO
import pandas as pd


def generate_qr_code(data: str) -> BytesIO:
    """Sinh mã QR trả về đối tượng BytesIO dạng ảnh PNG."""
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


def parse_excel_sheet(file_stream=None, sheet_url=None) -> pd.DataFrame:
    """Đọc file .xlsx hoặc Google Sheets trả về DataFrame."""
    if file_stream and sheet_url:
        raise ValueError("Vui lòng chỉ chọn 1 phương thức nhập liệu")
    elif sheet_url:
        from google_sheets import get_google_sheet
        return pd.DataFrame(get_google_sheet(sheet_url))
    else:
        df = pd.read_excel(file_stream, sheet_name='THÔNG TIN', skiprows=2)

        # Chuẩn hóa tên cột
        df.columns = [
            'STT', 'TÊN_THÁNH', 'HỌ', 'TÊN', 'HỌ_TÊN', 'NGÀY_SINH', 'GIÁO_XỨ',
            'RỬA_TỘI', 'RƯỚC_LỄ', 'THÊM_SỨC', 'ĐỊA_CHỈ', 'Phường', 'Quận',
            'TÊN_CHA', 'SĐT_CHA', 'TÊN_MẸ', 'SĐT_MẸ', 'TÊN_GH', 'SĐT_GH', 'GHI_CHÚ', 'code'
        ]

        # Xử lý ngày tháng
        date_columns = ['NGÀY_SINH', 'RỬA_TỘI', 'RƯỚC_LỄ', 'THÊM_SỨC']
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True).dt.date
            if df[col].isnull().any():
                raise ValueError(f"Cột {col} có giá trị ngày không hợp lệ")

        # Ghép địa chỉ
        df['ĐỊA_CHỈ'] = df['ĐỊA_CHỈ'].astype(str) + ', ' + df['Phường'].astype(str) + ', ' + df['Quận'].astype(str)

        df['SĐT_CHA'] = df['SĐT_CHA'].apply(lambda x: re.sub(r'\D', '', str(x)))
        df['SĐT_MẸ'] = df['SĐT_MẸ'].apply(lambda x: re.sub(r'\D', '', str(x)))
        df['SĐT_GH'] = df['SĐT_GH'].apply(lambda x: re.sub(r'\D', '', str(x)))

        return df

    return df
