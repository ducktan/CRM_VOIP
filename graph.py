import pandas as pd
import plotly.graph_objects as go

# Dữ liệu mẫu RFM
data = [
    {
        "Customer Name": "Minh Trần Giáp",
        "F Score": 2,
        "Frequency (F)": 3,
        "Last Purchase Date": "2024-11-09T03:00:00+03:00",
        "M Score": 4,
        "Monetary (M)": 4553000,
        "R Score": 5,
        "Recency (R)": 0,
        "Segment": "Promising",
        "Total Spending": 4553000
    },
    {
        "Customer Name": "Hà Phạm Thị",
        "F Score": 1,
        "Frequency (F)": 2,
        "Last Purchase Date": "2024-09-05T03:00:00+03:00",
        "M Score": 3,
        "Monetary (M)": 3959000,
        "R Score": 2,
        "Recency (R)": 65,
        "Segment": "About To Sleep",
        "Total Spending": 3959000
    },
    {
        "Customer Name": "Bình Hồ Hồng",
        "F Score": 1,
        "Frequency (F)": 1,
        "Last Purchase Date": "2024-11-09T03:00:00+03:00",
        "M Score": 2,
        "Monetary (M)": 2580000,
        "R Score": 5,
        "Recency (R)": 0,
        "Segment": "Recent Customers",
        "Total Spending": 2580000
    }
]

# Chuyển đổi dữ liệu thành DataFrame
df = pd.DataFrame(data)

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
fig.show()
