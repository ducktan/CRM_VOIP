from flask import Flask, render_template
from demo1 import get_rfm_data
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def rfm():
    # Lấy dữ liệu phân tích RFM
    rfm_data = get_rfm_data()
    # Chuyển đổi dữ liệu thành DataFrame
    df = pd.DataFrame(rfm_data)

    # Tạo bảng
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])

    # Cấu hình tiêu đề cho bảng
    fig.update_layout(title="Bảng Phân Khúc Khách Hàng RFM")

    # Chuyển đổi figure thành HTML
    table_html = pio.to_html(fig, full_html=False)

    # Render HTML với bảng
    return render_template('index.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
