import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# set style visualisasi
sns.set_theme(style="whitegrid")

# 1. LOAD DATA
@st.cache_data
def load_data():
    # Menempatkan folder tempat dashboard.py
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Menggabungkan folder dengan nama file
    file_path = os.path.join(current_dir, 'main_data.csv')

    # Membaca data
    df = pd.read_csv(file_path)

    # Konversi dteday ke datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

bike_df = load_data()

# 2. HEADER DASHBOARD
st.title('Bike Sharing Analysis Dashboard')
st.markdown("""Dashboard yang menganalisis pola penyewaan sepeda berdasarkan waktu, hari kerja, dan kondisi cuaca.""")

# 3. SIDEBAR FILTER
st.sidebar.header("Filter Data")

# Filter tanggal
min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()

with st.sidebar:
    st.write("**Rentang Waktu**")
    st.write("**Yang sudah disesuaikan menurut data aktual dataset :**")
    # Mengambil start_date & end_date dari date_input
    date_range = st.date_input(
        label='Pilih tanggal (Klik awal dan akhir)', 
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        label_visibility="collapsed"
    )

    # Validasi agar tidak error jika hanya 1 tanggal yang dipilih
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
        st.info("Silahkan pilih tanggal awal dan akhir.")

# Filter data berdasarkan tanggal
main_df = bike_df[(bike_df["dteday"] >= str(start_date)) & 
                  (bike_df["dteday"] <= str(end_date))]

# Filter Musim (Season)
season_options = main_df['season_label'].unique()
selected_season = st.sidebar.multiselect(
    'Pilih Musim:', 
    options=season_options,
    default=season_options
)

main_df = main_df[main_df['season_label'].isin(selected_season)]

# Jika data kosong karena filter musim di kosongkan
if main_df.empty:
    st.warning("Data tidak ditemukan. Silahkan pilih minimal satu musim di sidebar.")
    st.stop()

# 4. METRICS (ANGKA RINGKASAN)
st.subheader('Ringkasan Penyewaan Sepeda')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,.0f}")

with col2:
    avg_rentals = main_df['cnt'].mean()
    st.metric("Rata-rata per Jam", value=f"{avg_rentals:.1f}")

with col3:
    max_rentals = main_df['cnt'].max()
    st.metric("Penyewaan Tertinggi (1 Jam)", value=f"{max_rentals:,.0f}")

st.markdown("---")

# 5. VISUALISASI PERTANYAAN 1 (HARI KERJA VS HARI LIBUR)
st.subheader('1. Pola Penyewaan Berdasarkan Hari Kerja & Hari Libur')

if main_df.empty:
    st.warning("Tidak ada data pada rentang waktu/musim yang dipilih. Silahkan sesuaikan filter di sidebar.")
else:
    # Data preparation
    p1_data = main_df.groupby(by=['workingday', 'hr'])['cnt'].mean().reset_index()
    p1_data['Tipe Hari'] = p1_data['workingday'].map({0: 'Hari Libur/Akhir Pekan', 1: 'Hari Kerja'})

    fig1, ax1 = plt.subplots(figsize=(12, 6))

    # Menggunakan dictionary pada palette aar tidak error jika salah satu kategori hilang karena filter
    sns.lineplot(data=p1_data, x='hr', y='cnt', hue='Tipe Hari', palette={'Hari Kerja': '#33C1FF', 'Hari Libur/Akhir Pekan': '#FF5733'}, linewidth=2.5, ax=ax1)

    ax1.set_title('Perbandingan Rata-rata Penyewaan Sepeda per Jam', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Jam (0-23)', fontsize=12)
    ax1.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
    ax1.set_xticks(np.arange(0, 24, 2))
    plt.tight_layout()
    st.pyplot(fig1)

    st.info("**Insight:** Secara keseluruhan, pada hari kerja terjadi lonjakan pada pukul 08:00 dan 17:00-18:00 (jam berangkat/pulang kerja). Pada hari libur, penyewaan memuncak di siang hari (10:00-15:00). Dapat dilihat difilter musim manapun untuk melihat volume penyewaannya.")

st.markdown("---")

# 6. VISUALISASI PERTANYAAN 2 (PENGARUH CUACA)
st.subheader('2. Pengaruh Kondisi Cuaca (Musim Panas 2012)')

# Filter khusus Summer 2012 untuk grafik ini
summer_2012 = main_df[(main_df['season_label'] == 'Summer') & (main_df['year_label'] == 2012)]

# Mengecek apakah data Summer 2012 tersedia setelah difilter
if summer_2012.empty:
    st.warning("Data untuk Musim Panas (Summer) tahun 2012 tidak ditemukan pada filter yang anda pilih karena kebutuhan pertanyaan bisnis, Silahkan pilih 'Summer' pada filter musim di sidebar untuk melihat grafik ini.")
else:
    p2_data = summer_2012.groupby(by='weather_label')['cnt'].mean().reset_index().sort_values(by='cnt', ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=p2_data, x='weather_label', y='cnt', hue='weather_label', palette='Blues_r', legend=False, ax=ax2)
    ax2.set_title('Rata-rata Penyewaan Berdasarkan Cuaca (Summer 2012)', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax2.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)

    # Tambah label angka
    for index, row in enumerate(p2_data['cnt']):
        ax2.text(index, row + 5, round(row, 1), color='black', ha="center", fontsize=11, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig2)

    st.info("**Insight:** Cuaca cerah menghasilkan penyewaan tertinggi, sedangkan hujan ringan/salju menurunkan permintaan secara drastis.")

st.markdown("---")

# 7. ANALISIS LANJUTAN (BINNING / HEATMAP)
st.subheader('3. Segmentasi Tingkat Permintaan (Analisis Binning)')
st.write("Visualisasi ini menggunakan teknik *binning* untuk mengelompokkan tingkat permintaan menjadi **Rendah**, **Sedang**, **Tinggi**.")

if main_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Silahkan ubah filter di sidebar.")
else:
    # Binning
    q1 = main_df['cnt'].quantile(0.33)
    q2 = main_df['cnt'].quantile(0.66)

    # Menggunakan float('inf) sebagai batas agar tidak error jika nilai max berubah-ubah
    main_df['demand_category'] = pd.cut(
        main_df['cnt'],
        bins=[-1, q1, q2, float('inf')],
        labels=['Rendah', 'Sedang', 'Tinggi']
    )

    weekday_map = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    main_df['weekday_label'] = main_df['weekday'].map(weekday_map)

    # Pivot
    pivot_binning = main_df.groupby(['weekday_label', 'hr'])['demand_category'].agg(lambda x: x.mode()[0] if not x.mode().empty else np.nan).unstack()
    day_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    pivot_binning = pivot_binning.reindex(day_order)

    # Pivot Heatmap
    fig3, ax3 = plt.subplots(figsize=(14, 6))
    heatmap_data = pivot_binning.apply(lambda x: x.map({'Rendah': 1, 'Sedang': 2, 'Tinggi': 3})).astype(float)

    sns.heatmap(heatmap_data, cmap='YlOrRd', cbar_kws={'label': 'Tingkat Permintaan (1=Rendah, 2=Sedang, 3=Tinggi)'}, linewidths=.5, ax=ax3)
    ax3.set_title('Segmentasi Tingkat Permintaan berdasarkan Hari dan Jam', fontsize=14, fontweight='bold', pad=15)
    ax3.set_xlabel('Jam (0-23)', fontsize=12)
    ax3.set_ylabel('Hari', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig3)

    st.info("**Insight:** Secara umum, permintaan 'Tinggi' (warna oranye/merah) terkonsentrasi pada jam sibuk di hari kerja, dan bergeser ke siang hari pada akhir pekan.")

st.markdown("---")

# Footer
st.caption('Copyright (c) 2026 - Dicoding Submission')
