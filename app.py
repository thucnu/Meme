import streamlit as st
from duckduckgo_search import DDGS

# --- 1. CẤU HÌNH GIAO DIỆN (Làm đẹp) ---
st.set_page_config(
    page_title="Meme God - Trợ Lý Hài Hước",
    page_icon="🦄",  # Icon tab trình duyệt
    layout="centered"
)

# Thêm CSS để chỉnh màu nút bấm thành màu hồng/cam cho dễ thương
st.markdown("""
    <style>
    .stButton>button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff5252;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM TÌM KIẾM (Logic chính) ---
# --- Thay thế toàn bộ hàm tim_meme cũ bằng hàm này ---
def tim_meme(text_tinh_huong):
    # Đổi cách tạo từ khóa đơn giản hơn chút để dễ ra kết quả
    tu_khoa = f"{text_tinh_huong} meme"
    
    print(f"dang tim kiem voi tu khoa: {tu_khoa}") # Debug 1
    
    ket_qua_anh = []
    
    try:
        with DDGS() as ddgs:
            # Lấy 5 ảnh thôi để test cho nhanh
            results = ddgs.images(
                keywords=tu_khoa,
                region="wt-wt",
                safesearch="off",
                max_results=5
            )
            
            # Ép kiểu dữ liệu về list để kiểm tra xem có rỗng không
            results_list = list(results)
            
            print(f"So luong ket qua tim duoc: {len(results_list)}") # Debug 2
            
            if len(results_list) > 0:
                # In thử kết quả đầu tiên xem nó có cái key tên là 'image' không
                print("Du lieu anh dau tien:", results_list[0]) # Debug 3
            
            for r in results_list:
                # Cách lấy link an toàn hơn (nếu key 'image' sai thì nó không bị lỗi)
                url = r.get('image') 
                if url:
                    ket_qua_anh.append(url)
                    
    except Exception as e:
        print(f"Loi chi tiet: {e}") # Debug 4
        st.error(f"Ui chà, lỗi mạng hoặc thư viện: {e}")
        
    return ket_qua_anh
# --- 3. GIAO DIỆN NGƯỜI DÙNG (Frontend) ---

# Tiêu đề lớn
st.title("🦄 Meme God Online")
st.caption("Bạn kể khổ - Tôi tìm Meme!")

# Tạo một khung nhập liệu đẹp
with st.container():
    user_input = st.text_input(
        "Đang gặp chuyện gì dợ? (Ví dụ: OT không lương, Crush có bồ...)",
        placeholder="Gõ vào đây nè..."
    )
    
    # Nút bấm tìm kiếm
    btn_click = st.button("🔍 Tìm Meme Ngay")

# --- 4. XỬ LÝ KHI BẤM NÚT ---
if btn_click:
    if not user_input:
        st.warning("Ơ kìa, chưa nhập gì sao tìm được? 🥺")
    else:
        # Hiển thị vòng xoay "Đang tải"
        with st.spinner('Đang lặn lội khắp internet tìm ảnh... 🐢'):
            links = tim_meme(user_input)
            
            if links:
                st.success(f"Tìm thấy meme cho vụ: '{user_input}'")
                
                # Hiển thị ảnh dạng lưới (2 cột)
                col1, col2 = st.columns(2)
                
                for i, link in enumerate(links):
                    try:
                        if i % 2 == 0:
                            with col1:
                                st.image(link, use_column_width=True)
                        else:
                            with col2:
                                st.image(link, use_column_width=True)
                    except:
                        pass # Ảnh nào lỗi link thì bỏ qua
            else:
                st.info("Ca này khó quá, tìm không ra ảnh nào luôn 😭")

# Footer (Chân trang)
st.markdown("---")
st.markdown("<div style='text-align: center'>Made with 💖 by Python</div>", unsafe_allow_html=True)