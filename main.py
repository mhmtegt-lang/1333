import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sayfa Yapılandırması
st.set_page_config(page_title="Matematik Asistanı: Ondalık Sıralama", layout="centered")

st.title("👻 Hayalet Sıfırlarla Ondalık Sıralama")
st.write("Ondalık sayılarda basamak sayılarını eşitleyerek sıralama yapmayı öğrenelim!")

# Kullanıcı Girişi
st.sidebar.header("Sayıları Giriniz")
input_numbers = st.sidebar.text_input("Sayıları virgül (,) ile ayırarak yazın:", "9.56, 9.6, 9.7")

if input_numbers:
    # Sayıları temizle ve listeye al
    raw_list = [num.strip() for num in input_numbers.split(",")]
    
    # En uzun virgülden sonraki basamak sayısını bul
    max_decimal_places = 0
    for num in raw_list:
        if "." in num:
            places = len(num.split(".")[1])
            if places > max_decimal_places:
                max_decimal_places = places

    st.subheader("🛠️ Adım Adım Somutlaştırma")
    
    data = []
    for num in raw_list:
        parts = num.split(".")
        tam_kisim = parts[0]
        unda_birler = parts[1] if len(parts) > 1 else ""
        
        # Hayalet sıfırları ekleme (Padding)
        padded_num = f"{float(num):.{max_decimal_places}f}".replace(".", ",")
        original_num = num.replace(".", ",")
        
        data.append({
            "Orijinal Sayı": original_num,
            "Basamak Eşitlenmiş (Hayalet Sıfırlı)": padded_num,
            "Değer": float(num)
        })

    # Tabloyu Göster
    df = pd.DataFrame(data)
    st.table(df[["Orijinal Sayı", "Basamak Eşitlenmiş (Hayalet Sıfırlı)"]])

    st.info(f"**💡 Pedagojik Not:** Tüm sayıların virgülden sonra **{max_decimal_places}** basamağı olacak şekilde sonuna '0' ekledik. Bu, sayıların değerini değiştirmez, sadece kıyaslamayı kolaylaştırır.")

    # Sıralama Sonucu
    sorted_df = df.sort_values(by="Değer")
    
    st.success("### ✅ Küçükten Büyüğe Sıralama")
    result_str = " < ".join(sorted_df["Basamak Eşitlenmiş (Hayalet Sıfırlı)"].tolist())
    st.latex(result_str)

    # Görselleştirme
    st.bar_chart(df.set_index("Orijinal Sayı")["Değer"])
