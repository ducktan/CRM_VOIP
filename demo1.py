import requests
from datetime import datetime

def segment_customer(r_score, f_score, m_score):
    # Tạo bộ ba RFM dưới dạng chuỗi để dễ so sánh
    rfm_combination = f"{r_score}{f_score}{m_score}"

    # Phân loại khách hàng theo bộ ba RFM
    if rfm_combination in ["555", "554", "544", "545", "454", "455", "445"]:
        return "Champion"
    elif rfm_combination in ["543", "444", "435", "355", "354", "345", "344", "335"]:
        return "Loyal Customer"
    elif rfm_combination in ["553", "551", "552", "541", "542", "533", "532", "531", 
                             "452", "451", "442", "441", "431", "453", "433", "432", 
                             "423", "353", "352", "351", "342", "341", "333", "323"]:
        return "Potential Loyalist"
    elif rfm_combination in ["512", "511", "422", "421", "412", "411", "311"]:
        return "Recent Customers"
    elif rfm_combination in ["525", "524", "523", "522", "521", "515", "514", "513", 
                             "425", "424", "413", "414", "415", "315", "314", "313"]:
        return "Promising"
    elif rfm_combination in ["535", "534", "443", "434", "343", "334", "325", "324"]:
        return "Customers Needing Attention"
    elif rfm_combination in ["331", "321", "312", "221", "213"]:
        return "About To Sleep"
    elif rfm_combination in ["255", "254", "245", "244", "253", "252", "243", "242", 
                             "235", "234", "225", "224", "153", "152", "145", "143", 
                             "142", "135", "134", "133", "125"]:
        return "At Risk"
    elif rfm_combination in ["155", "154", "144", "214", "215", "115", "114", "113", "124"]:
        return "Can't Lose Them"
    elif rfm_combination in ["332", "322", "231", "241", "251", "233", "232", "223", 
                             "222", "132", "123", "122", "212", "211"]:
        return "Hibernating"
    elif rfm_combination in ["111", "112", "121", "131", "141", "151"]:
        return "Lost"
    else:
        return "Uncategorized"

def get_rfm_data():
    # Webhook URL của bạn để lấy thông tin giao dịch (deals)
    deal_webhook_url = 'https://b24-kry63g.bitrix24.vn/rest/1/in0hmm11yuquk8hh/crm.deal.list.json'

    # Gửi yêu cầu GET để lấy thông tin giao dịch (deals)
    response = requests.get(deal_webhook_url)

    # Kiểm tra kết quả từ API
    if response.status_code == 200:
        deals = response.json()
        
        # Lọc các giao dịch có STAGE_ID là 'WON'
        won_deals = [deal for deal in deals['result'] if deal.get('STAGE_ID') == 'WON']

        current_date = datetime.now()
        customer_deals_dict = {}

        # Tạo một dictionary để gộp các giao dịch của cùng một khách hàng
        for deal in won_deals:
            contact_id = deal.get('CONTACT_ID')
            close_date = deal.get('CLOSEDATE')
            amount_spent = float(deal.get('OPPORTUNITY', 0))

            # Kiểm tra nếu contact_id đã có trong dictionary, nếu có thì gộp lại
            if contact_id not in customer_deals_dict:
                customer_deals_dict[contact_id] = {
                    'Customer Name': "",
                    'Deals': [],
                    'Total Spending': 0.0
                }

            # Thêm giao dịch vào danh sách của khách hàng
            customer_deals_dict[contact_id]['Deals'].append(deal)
            customer_deals_dict[contact_id]['Total Spending'] += amount_spent

        rfm_data = []
        for contact_id, customer_data in customer_deals_dict.items():
            # Lấy thông tin khách hàng từ CONTACT_ID
            contact_webhook_url = f'https://b24-kry63g.bitrix24.vn/rest/1/in0hmm11yuquk8hh/crm.contact.get.json?ID={contact_id}'
            contact_response = requests.get(contact_webhook_url)
            
            if contact_response.status_code == 200:
                contact_data = contact_response.json()
                contact_name = contact_data['result'].get('NAME') + ' ' + contact_data['result'].get('LAST_NAME')
            else:
                contact_name = "Không tìm thấy tên khách hàng"

            # Tính điểm Recency (R): Ngày mua gần nhất
            latest_deal = max(customer_data['Deals'], key=lambda x: x['CLOSEDATE'])
            close_date = latest_deal['CLOSEDATE']
            close_date_obj = datetime.strptime(close_date, "%Y-%m-%dT%H:%M:%S+03:00")
            days_since_last_purchase = (current_date - close_date_obj).days

            # Tính điểm Frequency (F): Số lần giao dịch của khách hàng
            frequency_value = len(customer_data['Deals'])

            # Tính điểm Monetary (M): Tổng số tiền chi tiêu của khách hàng
            total_spending = customer_data['Total Spending']

            # Phân loại điểm cho R, F, M
            r_score = 5 if days_since_last_purchase < 7 else \
                      4 if days_since_last_purchase < 30 else \
                      3 if days_since_last_purchase < 60 else \
                      2 if days_since_last_purchase < 120 else \
                      1 if days_since_last_purchase < 216 else 0

            f_score = 5 if frequency_value >= 10 else \
                      4 if frequency_value >= 8 else \
                      3 if frequency_value >= 5 else \
                      2 if frequency_value >= 3 else \
                      1

            m_score = 5 if total_spending >= 5000000 else \
                      4 if total_spending >= 4000000 else \
                      3 if total_spending >= 3000000 else \
                      2 if total_spending >= 2000000 else \
                      1
            

            segmentCustomer = segment_customer(r_score, f_score, m_score)

            # Thêm vào danh sách RFM
            rfm_data.append({
                'Customer Name': contact_name,
                'Recency (R)': days_since_last_purchase,
                'Frequency (F)': frequency_value,
                'Monetary (M)': total_spending,
                'R Score': r_score,
                'F Score': f_score,
                'M Score': m_score,
                'Last Purchase Date': close_date,
                'Total Spending': total_spending,
                'Segment': segmentCustomer
            })

        return rfm_data
    else:
        return {"Error": f"Error: {response.status_code}"}
