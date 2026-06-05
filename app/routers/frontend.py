import streamlit as st
import requests
import pandas as pd
import numpy as np

# Mengatur tampilan layar menjadi lebar (wide)
st.set_page_config(page_title="Retail Demand Predictor", layout="wide")

st.title("🛒 Retail Demand Prediction Dashboard")
st.write("Aplikasi cerdas untuk memprediksi jumlah permintaan produk dan mengoptimalkan persediaan gudang.")
st.markdown("---")

# Membuat Form Input
with st.form("form_prediksi"):
    st.subheader("📝 Masukkan Data Transaksi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.number_input("Tahun (Year)", min_value=2000, max_value=2100, value=2026)
        month = st.number_input("Bulan (Month)", min_value=1, max_value=12, value=6)
        item_type = st.text_input("Tipe Barang (Item Type)", value="Elektronik")
        
    with col2:
        retail_transfers = st.number_input("Transfer Retail (Unit)", min_value=0.0, value=10.0)
        warehouse_sales = st.number_input("Penjualan Gudang (Unit)", min_value=0.0, value=100.0)
        
    submitted = st.form_submit_button("Prediksi Permintaan 🚀")

if submitted:
    data_input = {
        "year": int(year),
        "month": int(month),
        "item_type": item_type,
        "retail_transfers": float(retail_transfers),
        "warehouse_sales": float(warehouse_sales)
    }
    
    API_URL = "http://127.0.0.1:8000/api/v1/predict" 
    
    with st.spinner('AI sedang menganalisis data...'):
        try:
            response = requests.post(API_URL, json=data_input)
            
            if response.status_code == 200:
                hasil = response.json()
                
                # Mengambil angka prediksi asli (yang ada komanya)
                prediksi_asli = hasil["predicted_retail_sales"]
                nama_model = hasil["model_used"]
                
                # MEMBULATKAN ANGKA MENJADI BILANGAN BULAT
                prediksi_bulat = int(round(prediksi_asli))
                
                st.success("Tadaa! Prediksi Berhasil Dihitung! 🎉")
                
                # --- BAGIAN TAMPILAN DASHBOARD ---
                
                # 1. Menampilkan Kartu Angka Utama (Menggunakan angka bulat)
                st.metric(label=f"Estimasi Permintaan: {item_type}", value=f"{prediksi_bulat} Unit", delta="Target Restock")
                st.info(f"💡 Dihitung menggunakan algoritma AI: **{nama_model}**")
                
                st.markdown("---")
                st.subheader("📊 Analisis Visual")
                
                # Membagi layar menjadi 2 kolom untuk grafik
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.markdown("**Perbandingan Aktivitas vs Prediksi**")
                    # Membuat Dataframe untuk Bar Chart
                    df_bar = pd.DataFrame({
                        "Kategori": ["Transfer Retail", "Penjualan Gudang", "Prediksi Permintaan"],
                        "Jumlah Unit": [retail_transfers, warehouse_sales, prediksi_bulat]
                    }).set_index("Kategori")
                    
                    # Menampilkan Bar Chart
                    st.bar_chart(df_bar, color="#FF4B4B")
                    
                with col_chart2:
                    st.markdown("**Tren Permintaan 6 Bulan (Simulasi)**")
                    # Membuat simulasi data historis (5 bulan ke belakang + 1 bulan prediksi)
                    # Menggunakan int() agar data tren juga berupa bilangan bulat
                    trend_data = [max(0, int(prediksi_bulat + np.random.uniform(-15, 15))) for _ in range(5)]
                    trend_data.append(prediksi_bulat) # Memasukkan hasil prediksi bulan ini
                    
                    df_line = pd.DataFrame({
                        "Bulan": ["Bln -5", "Bln -4", "Bln -3", "Bln -2", "Bln -1", "Bulan Ini (Prediksi)"],
                        "Permintaan": trend_data
                    }).set_index("Bulan")
                    
                    # Menampilkan Line Chart
                    st.line_chart(df_line, color="#29B5E8")
                
            else:
                st.error("Gagal memproses data. Cek input atau koneksi server.")
                
        except requests.exceptions.ConnectionError:
            st.error("Gagal terhubung ke server! Pastikan FastAPI sudah menyala di http://127.0.0.1:8000")