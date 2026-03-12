import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Hayalet Sıfır Avı", layout="centered")

st.title("👻 Hayalet Sıfırlarla Ondalık Sıralama")
st.markdown("### Sayıları karşılaştırmak için basamakları eşitleyelim!")

# Kullanıcı Girişi - Daha net yönerge
st.sidebar.header("🔢 Veri Girişi")
input_numbers = st.sidebar.text_input(
    "Sayıları boşluk bırakarak yazın:", 
    "9,56 9,6 9,7",
    help="Örn: 5,2 5,12 5,3"
)

if input_numbers:
    # 1. ADIM: Sayıları ayır (Boşluk veya Noktalı Virgül baz alınır)
    # Virgülü ayırıcı olarak kullanmıyoruz ki 9,56 bölünmesin!
    raw_list = re.split(r'[;\s]+', input_numbers.strip())
    
    # 2. ADIM: Türkçe virgülü (.) noktaya çevirip sayıya dönüştür
    clean_data = []
    for num in raw_list:
        if num:
            try:
                dot_num = num.replace(",", ".")
                clean_data.append({"orig": num, "val": float(dot_num)})
            except ValueError:
                continue

    if clean_data:
        # En uzun ondalık basamağı bul
        max_p = 0
        for item in clean_data:
            s_num = str(item['val'])
            if "." in s_num:
                p = len(s_num.split(".")[1])
                if p > max_p: max_p = p

        # Veriyi Hazırla ve Hayalet Sıfırları Vurgula
        display_list = []
        for item in clean_data:
            # Sayıyı hedeflenen basamak sayısına tamamla
            padded = f"{item['val']:.{max_p}f}".replace(".", ",")
            orig = item['orig'].replace(".", ",")
            
            # Hayalet sıfırları belirgin yap (Kalın yazarak)
            diff = len(padded) - len(orig)
            ghost_view = orig + f"**{padded[-diff:]}**" if diff > 0 else padded
            
            display_list.append({
                "Orijinal Sayı": orig,
                "Hayalet Sıfırlı Hali": ghost_view,
                "Sayısal Değer": item['val']
            })

        st.subheader("📊 Adım Adım Somutlaştırma")
        df = pd.DataFrame(display_list)
        
        # Tabloyu markdown ile daha şık gösterelim (HTML desteğiyle)
        st.write("Aşağıdaki tabloda eklenen **'Hayalet Sıfırlar'** kalın harflerle gösterilmiştir:")
        st.table(df[["Orijinal Sayı", "Hayalet Sıfırlı Hali"]])

        # 3. ADIM: Sıralama
        sorted_df = df.sort_values(by="Sayısal Değer")
        
        st.success("### ✅ Küçükten Büyüğe Sıralama")
        # LaTeX formatında temiz sıralama
        order_latex = " < ".join([x.replace("**", "") for x in sorted_df["Hayalet Sıfırlı Hali"]])
        st.latex(order_latex)

        # Grafik
        st.bar_chart(df.set_index("Orijinal Sayı")["Sayısal Değer"])
    else:
        st.warning("Lütfen geçerli sayılar girin.")
