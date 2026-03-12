import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# Sayfa Ayarları
st.set_page_config(page_title="Matematik Asistanı | Ondalık Sıralama", layout="centered")

st.title("👻 Hayalet Sıfırlarla Ondalık Sıralama")
st.markdown("""
Bu uygulama, ondalık sayılarda **basamak eşitleme** mantığını somutlaştırmak için tasarlanmıştır. 
Sayıların sonuna eklenen '0'lar, onların değerini değiştirmez ama kıyaslamayı kolaylaştırır!
""")

# Yan Panel - Veri Girişi
st.sidebar.header("🔢 Sayı Girişi")
input_text = st.sidebar.text_input(
    "Sayıları boşluk bırakarak yazın:", 
    "9,56 9,6 9,7",
    help="Örn: 1,2 1,25 1,3"
)

if input_text:
    # 1. Veri Temizleme (Boşluk veya noktalı virgülden ayır, virgülü noktaya çevir)
    raw_list = re.split(r'[;\s]+', input_text.strip())
    clean_data = []
    
    for r in raw_list:
        if r:
            try:
                dot_val = r.replace(",", ".")
                clean_data.append({"original": r, "value": float(dot_val)})
            except ValueError:
                continue

    if clean_data:
        # En uzun ondalık basamak sayısını bul
        max_p = 0
        for item in clean_data:
            s_val = str(item['value'])
            if "." in s_val:
                p = len(s_val.split(".")[1])
                if p > max_p: max_p = p

        # Veri Hazırlama ve Hayalet Sıfır Vurgusu
        processed_list = []
        for item in clean_data:
            padded = f"{item['value']:.{max_p}f}".replace(".", ",")
            orig = item['original'].replace(".", ",")
            
            # Farkı bulup hayalet sıfırları kalınlaştıralım
            diff_len = len(padded) - len(orig)
            ghost_display = orig + f"**{padded[-diff_len:]}**" if diff_len > 0 else padded
            
            processed_list.append({
                "Orijinal": orig,
                "Hayalet Sıfırlı": ghost_display,
                "Değer": item['value'],
                "Display": padded
            })

        df = pd.DataFrame(processed_list)

        # AŞAMA 1: Tablo Gösterimi
        st.subheader("📊 1. Adım: Basamakları Eşitleyelim")
        st.write("Eklenen **Hayalet Sıfırlar** kalın harflerle gösterilmiştir:")
        st.table(df[["Orijinal", "Hayalet Sıfırlı"]])

        # AŞAMA 2: Karşılaştırmalı Grafik (Zoomed-In)
        st.subheader("📈 2. Adım: Büyüklükleri Kıyaslayalım")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        # Farkı belirgin yapmak için Y eksenini daraltıyoruz
        min_v, max_v = df["Değer"].min(), df["Değer"].max()
        ax.set_ylim(min_v - 0.05, max_v + 0.05) 
        
        colors = ['#87CEEB', '#4682B4', '#000080']
        bars = ax.bar(df["Orijinal"], df["Değer"], color=colors[:len(df)])
        
        # Bar üzerine değerleri yazma
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}'.replace(".", ","),
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title("Sayıların Büyüklük Farkı (Yakınlaştırılmış)")
        st.pyplot(fig)

        # AŞAMA 3: Sayı Doğrusu (Pedagojik Model)
        st.subheader("📍 3. Adım: Sayı Doğrusunda Görelim")
        
        fig2, ax2 = plt.subplots(figsize=(10, 2))
        ax2.set_xlim(min_v - 0.1, max_v + 0.1)
        ax2.set_ylim(-1, 1)
        ax2.axhline(0, color='black', linewidth=1) # Ana çizgi
        
        for index, row in df.iterrows():
            ax2.plot(row['Değer'], 0, 'ro', markersize=10)
            ax2.text(row['Değer'], 0.3, row['Display'], ha='center', fontweight='bold', color='darkblue')
            ax2.vlines(row['Değer'], -0.2, 0, colors='red', linestyles='--')

        ax2.get_yaxis().set_visible(False)
        st.pyplot(fig2)

        # AŞAMA 4: Sonuç
        sorted_df = df.sort_values(by="Değer")
        st.success("### ✅ Küçükten Büyüğe Sıralama")
        result_latex = " < ".join(sorted_df["Display"].tolist())
        st.latex(result_latex)

    else:
        st.info("Lütfen aralarında boşluk bırakarak ondalık sayılar girin (Örn: 9,56 9,6).")
