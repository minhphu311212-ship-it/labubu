import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser
st.sidebar.title("🎶 Danh sách nghệ sĩ")
selected_artist = st.sidebar.radio("Chọn nghệ sĩ:", ["Yorushika", "buitruonglinh", "Sơn Tùng M-TP",])

videos = {
    "Yorushika": [
        ("だから僕は音楽を辞めた", "https://www.youtube.com/watch?v=KTZ-y85Erus"),
        ("言って。", "https://www.youtube.com/watch?v=F64yFFnZfkI"),
        ("春泥棒", "https://www.youtube.com/watch?v=Sw1Flgub9s8 "),
      
    ],
    "buitruonglinh": [
        ("Giờ Thì", "https://www.youtube.com/watch?v=69ZDBWoj5YM"),
        ("Yêu Người Có Ưóc Mơ", "https://www.youtube.com/watch?v=6r7jzy1LABY"),
        ("Đường Tôi Chở Em Về", "https://www.youtube.com/watch?v=OuNo8Tkb3lI"),
     ],
    "Sơn Tùng M-TP": [
        ("Lạc trôi", "https://www.youtube.com/watch?v=Llw9Q6akRo4"),
        ("Chúng ta không thuộc về nhau", "https://www.youtube.com/watch?v=GQRU3SRbaYw"),
        ("Muộn rồi mà sao còn", "https://www.youtube.com/watch?v=yzpzm15wMPY"),
        ("Hãy trao cho anh", "https://www.youtube.com/watch?v=knW7-x7Y7RE")
    ]
}

st.title("🎧 Ứng dụng giải trí và sức khỏe")

tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["🎤 MV yêu thích", "💤 Dự đoán giờ ngủ", "📰 Đọc báo", "Kiểm tra sức khỏe", "Sports", "Thời gian đi ngủ"])

with tab1:
    st.header(f"Các bài hát của {selected_artist} 🎵")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)
        
with tab2:
    st.header("💤 Dự đoán giờ ngủ mỗi đêm")
    # Tuổi, mức độ hoạt động thể chất, thời gian dùng máy tính
    x = [
        [10, 1, 8],
        [20, 5, 6],
        [25, 8, 3],
        [30, 6, 5],
        [35, 2, 9],
        [40, 4, 3]
    ]
    y = [10, 8, 6, 7, 9.5, 9]
    model = LinearRegression()
    model.fit(x,y)

    st.write("Nhập thông tin cá nhân: ")
    age = st.number_input("Tuổi của bạn", min_value= 5, max_value=100, value=25)
    activity = st.slider("Mức độ hoạt động thể chất (1 = ít, 10 = rất nhiều)", 1, 10, 5)
    screen_time = st.number_input("Thời gian dùng màn hình trong 1 ngày (giờ)", min_value=0, max_value=24, value=6)

    if st.button("Dự đoán ngay "):
        input_data = [[age, activity, screen_time]]
        result = model.predict(input_data)[0]
        st.success(f"Bạn nên ngủ khoảng {result:.1f} giờ mỗi đêm")

        if result < 6.5:
            st.warning("Có thể bạn cần nghỉ ngơi nhiều hơn để cải thiện sức khỏe. ")
        elif result > 9:
            st.info("Có thể bạn đang vận động nhiều, bạn cần ngủ bù hợp lý nhé ")
        else:
            st.success("Lượng ngủ lý tưởng, hãy giữ thói quen tốt ")
        
with tab3:
    st.header("📰 Tin tức mới nhất từ VnExpress")
    tabA, tabB = st.tabs(["📰 Tin tức mới nhất từ VnExpress", "💰 Cập nhật giá vàng từ Vietnamnet"])
    with tabA:
        feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    for entry in feed.entries[:5]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)
    with tabB:
        st.header("💰 Cập nhật giá vàng từ Vietnamnet")

    feed = feedparser.parse("https://vietnamnet.vn/rss/kinh-doanh.rss")
    gold_news = [entry for entry in feed.entries if "vàng" in entry.title.lower() or "giá vàng" in entry.summary.lower()]

    if gold_news:
        for entry in gold_news[:5]:  # Hiện 5 bài gần nhất
            st.subheader(entry.title)
            st.write(entry.published)
            st.write(entry.link)
    else:
        st.warning("Không tìm thấy bản tin giá vàng gần đây.")

    with tab4: 
        tabC, tabD, tabE = st.tabs(["💪 Tính chỉ số BMI của bạn", "Khuyến nghị lượng nước uống mỗi ngày", "Số bước chân cần đi mỗi ngày"])
    with tabC:
        st.header("💪 Tính chỉ số BMI của bạn")
        st.write("Ứng dụng giúp bạn tính chỉ số **BMI (Body Mass Index)** để đánh giá tình trạng cơ thể.")
        col1, col2 = st.columns(2)
        with col1:
                weight = st.number_input("Cân nặng (kg)", min_value=1.0, step=0.1)
        with col2:
                height = st.number_input("Chiều cao (m)", min_value=0.5, step=0.01)
        bmi_min = 18.5
        bmi_max = 25
        weight_min = bmi_min * (height ** 2)
        weight_max = bmi_max * (height ** 2)
        if st.button("Tính BMI"):
                bmi = weight / (height ** 2)
                st.markdown(f"### 🧮 Kết quả: **{bmi:.2f}**")
                if bmi < 18.5:
                    st.info("➡️ Bạn **gầy** hơn mức bình thường.")
                    tang_can = bmi - bmi_min
                    can_them = bmi_min * (height ** 2) - weight
                    st.info(f"Bạn cần tăng ít nhất **{can_them:.1f} kg** để đạt BMI bình thường.")
                elif 18.5 <= bmi < 24.9:
                    st.success("✅ Bạn có **cân nặng bình thường**.")       
                elif 25 <= bmi < 29.9:
                    st.warning("⚠️ Bạn đang **thừa cân**.")
                    can_giam = weight - bmi_max * (height ** 2)
                    st.warning(f"Bạn cần giảm ít nhất **{can_giam:.1f} kg** để đạt BMI bình thường.")
                else:
                    st.error("🚨 Bạn đang ở mức **béo phì**.")
                    can_giam = weight - bmi_max * (height ** 2)
                    st.error(f"Bạn cần giảm ít nhất **{can_giam:.1f} kg** để đạt BMI bình thường.")
                    
    with tabD:
        st.title("Khuyến nghị lượng nước uống mỗi ngày")
        tuoi = st.number_input("Nhập tuổi của bạn:", min_value=1, max_value=100, value=18, step=1)
        if st.button("Kiểm tra lượng nước cần uống"):
            if tuoi < 4:
                st.info("Khuyến nghị: 1.3 lít/ngày")
            elif 4 <= tuoi <= 8:
                st.info("Khuyến nghị: 1.7 lít/ngày")
            elif 9 <= tuoi <= 13:
                st.info("Khuyến nghị: 2.1 đến 2.4 lít/ngày")
            elif 14 <= tuoi <= 18:
                st.info("Khuyến nghị: 2.3 đến 3.3 lít/ngày")
            elif 19 <= tuoi <= 50:
                st.info("Khuyến nghị: 2.7 lít/ngày đối với nữ, 3.7 lít/ngày đối với nam")
            elif tuoi > 50:
                st.info("Khuyến nghị: Khoảng 2.5 đến 3.0 lít/ngày (phụ thuộc vào sức khỏe và mức độ vận động)")
            else:
                st.warning("Vui lòng nhập độ tuổi hợp lệ.")
    with tabE:
        st.title("Số bước chân cần đi mỗi ngày")
        baonhieutuoi = st.number_input("Bạn bao nhiêu tuổi?", min_value=1, max_value=100, value=18, step=1)
        if st.button("Số bước chân cần đi:"):
            if baonhieutuoi < 18:
                st.info("Bạn nên đi **12.000-15.000 bước**mỗi ngày")
            elif 17 < baonhieutuoi <= 39:
                st.warning("Bạn nên đi **8.000-10.000 bước** mỗi ngày")
            elif 39 < baonhieutuoi <= 64:
                st.warning("Bạn nên đi **7.000-9.000 bước** mỗi ngày")
            elif baonhieutuoi > 64:
                st.warning("Bạn nên đi **6.000-8.000 bước** mỗi ngày")
            else:
                st.error("Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin")

with tab5:
    st.header("The lastest news from VNExpress")
    feed = feedparser.parse("https://vietnamnet.vn/rss/the-thao.rss")
    for entry in feed.entries[:10]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)

with tab6: 
    st.header('Kiem tra thoi gian di ngu ly tuong')
    tabA, tabB = st.tabs(['Tre so sinh/Moi tap di','Tre nho, nguoi lon'])
    with tabA:
        thang = st.number_input('Nhap so thang tuoi:', min_value=0, max_value=24, value=12, step=1)
        if st.button('tinh thoi gian di ngu theo thang tuoi'):
            if thang < 4:
                st.info('Thoi gian di ngu ly tuong: 14-17 gio/ dem')
            else:
                st.info('Thoi gian di ngu ly tuong: 12-16 gio/ dem')
    with tabB:
        tuoi = st.number_input('Nhap tuoi:', min_value=2, max_value=100, value=25, step=1)
        if st.button('tinh thoi gian can ngu'):
            if tuoi < 3:
                st.info('Thoi gian di ngu ly tuong: 11-14 gio/ dem')
            elif tuoi < 6:
                st.info('Thoi gian di ngu ly tuong: 10-13 gio/ dem')
            elif tuoi < 14:
                st.info('Thoi gian di ngu ly tuong: 9-11 gio/ dem')
            elif tuoi < 18:
                st.info('Thoi gian di ngu ly tuong: 8-10 gio/ dem')
            elif tuoi < 65:
                st.info('Thoi gian di ngu ly tuong: 7-9 gio/ dem')
            else:
                st.info('Thoi gian di ngu ly tuong: 7-8 gio/ dem')






                