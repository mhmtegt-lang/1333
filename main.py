import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hayalet Sıfır Avı", layout="centered")

st.title("👻 Hayalet Sıfırlarla Ondalık Sıralama")
st.write("Sayıları karşılaştırmak için basamakları eşitleyelim!")

# Kullanıcı Girişi
st.sidebar.header("Sayıları Giriniz")
# Hem virgül hem boşlukla ayırmayı desteklemek için ipucu ekledik
input_numbers = st.sidebar.text_input("Sayıları yazın (Örn: 5,2 5,12 5,3):", "9,56, 9,6, 9,7")

if input_numbers:
    # 1. TEMİZLİK: Girdiyi boşluklara veya virgüllere göre ayır
    import re
    # Virgül veya boşluk gördüğü her yerden böler
    raw_list = re.split(r'[,\s]+', input_numbers.strip())
    
    # 2. DÜZELTME: Türkçe virgülleri (.) noktaya çevir
    clean_list = [num.replace(",", ".") for num in raw_list if num]
    
    try:
        # En uzun virgülden sonraki basamak sayısını bul
        max_decimal_places = 0
        for num in clean_list:
            if "." in num:
                places = len(num.split(".")[1])
                if places > max_decimal_places:
                    max_decimal_places = places

        st.subheader("🛠️ Adım Adım Somutlaştırma")
        
        data = []
        for num in clean_list:
            val = float(num)
            # Hayalet sıfırları ekleme (Padding)
            padded_num = f"{val:.{max_decimal_places}f}".replace(".", ",")
            original_display = num.replace(".", ",")
            
            data.append({
                "Orijinal Sayı": original_display,
                "Hayalet Sıfırlı Hali": padded_num,
                "Sayısal Değer": val
            })

        df = pd.DataFrame(data)
        st.table(df[["Orijinal Sayı", "Hayalet Sıfırlı Hali"]])

        # Sıralama Sonucu
        sorted_df = df.sort_values(by="Sayısal Değer")
        st.success("### ✅ Küçükten Büyüğe Sıralama")
        result_str = " < ".join(sorted_df["Hayalet Sıfırlı Hali"].tolist())
        st.latex(result_str)
        
        st.bar_chart(df.set_index("Orijinal Sayı")["Sayısal Değer"])

    except ValueError:
        st.error("Lütfen sadece sayı girdiğinizden emin olun! (Örn: 5,2 5,3)")
