import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat data
data = pd.read_csv('Cleaned_Air_Quality.csv')

# Fungsi untuk menghasilkan deskripsi data
def generate_data_description(data):
    st.title("Deskripsi Data")
    st.subheader("Konteks")
    st.write("Pembacaan PM2.5 sering kali disertakan dalam laporan kualitas udara dari otoritas lingkungan dan perusahaan. PM2.5 merujuk pada materi partikulat (PM) di atmosfer yang memiliki diameter kurang dari 2,5 mikrometer. Dengan kata lain, ini digunakan sebagai ukuran polusi.")
    st.subheader("Konten")
    st.write("Kumpulan data ini mencakup data polutan udara per jam dari 12 lokasi pemantauan kualitas udara yang dikontrol secara nasional. Data kualitas udara berasal dari Pusat Pemantauan Lingkungan Kota Beijing. Data meteorologi di setiap lokasi kualitas udara dicocokkan dengan stasiun cuaca terdekat dari Administrasi Meteorologi China. Periode waktu yang digunakan adalah dari tanggal 1 Maret 2013 hingga 28 Februari 2017.")
    st.subheader("Ucapan Terima Kasih")
    st.write("Zhang, S., Guo, B., Dong, A., He, J., Xu, Z. and Chen, S.X. (2017) Cautionary Tales on Air-Quality Improvement in Beijing. Proceedings of the Royal Society A, Volume 473, No. 2205, Pages 20170457.")
    st.subheader("Dataset")
    st.write("File-file tersebut diunduh dari Repositori Pembelajaran Mesin UCI dan belum dimodifikasi. https://archive.ics.uci.edu/ml/datasets/Beijing+Data+Kualitas+Udara+Berbeda+Situs")
    st.write("Sedangkan file yang digunakan dalam visualisasi ini merupakan data yang telah dimodifikasi dan dibersihkan. https://drive.google.com/file/d/1sOC--PJWA4awH96iPEJyNCGrQEOoC6w-/view?usp=sharing")
    # Membuat checkbox jika user ingin melihat datanya
    if st.checkbox("Tampilkan Data"):
        st.write(data)
    # Membuat statistika deskriptif data
    st.write("Statistika Deskriptif Data:")
    st.write(data.describe())

# Function to generate boxplot
def generate_boxplot(data, selected_pollutant):
    st.title("Pola Musiman Untuk Tingkat Polusi Udara di Beijing")
    
    # Membuat data time series terlebih dahulu dengan mengelompokannya berdasarkan bulan
    data['date'] = pd.to_datetime(data['date'])
    data_time_series = data[['date', 'PM2.5', 'PM10']].set_index('date').resample('M').mean()

    # Sidebar
    st.sidebar.title("Filter")
    selected_pollutant = st.sidebar.selectbox("Pilih Polutan", ["PM2.5", "PM10"])

    # Membuat figure dan subplot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Boxplot untuk selected_pollutant
    sns.boxplot(x=data_time_series.index.month, y=data_time_series[selected_pollutant], color='b' if selected_pollutant == 'PM2.5' else 'g', width=0.2, ax=ax)
    ax.set_title(f"Konsentrasi Rata-rata Bulanan dari {selected_pollutant}")
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Konsentrasi')

    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("Di kutip dari laman https://www.guilinchina.net/travel-guide/beijing/weather/, musim di Beijing dapat dibagi menjadi berikut:")
    text = '''
    - **Musim Semi:** sekitar awal bulan **April** hingga minggu-minggu terakhir bulan **Mei**.
    - **Musim Panas:** sekitar minggu pertama bulan **Juni** hingga pertengahan **September**.
    - **Musim Gugur:** sekitar paruh akhir bulan **September** hingga **November**.
    - **Musim Dingin:** sekitar pertengahan **November** hingga **Maret**.
    '''
    st.write(text)

    # Menambahkan keterangan berbeda tergantung pada pilihan selectbox
    if selected_pollutant == "PM2.5":
        st.write("Puncak konsentrasi PM2.5 ada di sekitar bulan Desember hingga Februari, hal tersebut terjadi pada musim dingin. Namun perlahan mengalami penurunan pada musim semi, dan kembali naik pada musim panas. Meskipun pada musim panas tingkat konsentrasi PM2.5 tidak sebanyak musim dingin. Pada setiap bulan di musim gugur juga mengalami kenaikan tingkat konsentrasi PM2.5. Sehingga dapat disimpulkan bahwa pada akhir musim dingin hingga akhir musim panas terjadi penurunan tingkat konsentrasi PM2.5 yang signifikan, meskipun pada 2 bulan awal musim panas mengalami kenaikan.")     
    else:
        st.write("Puncak konsentrasi PM10 ada di sekitar bulan Desember hingga Februari, hal tersebut terjadi pada musim dingin. Namun perlahan mengalami penurunan pada musim semi, dan kembali naik pada musim panas. Pada setiap bulan di musim gugur juga mengalami kenaikan tingkat konsentrasi PM10. Sehingga dapat disimpulkan bahwa pada akhir musim dingin hingga akhir musim panas terjadi penurunan tingkat konsentrasi PM10 yang signifikan, meskipun pada 2 bulan awal musim panas mengalami kenaikan.")

# Fungsi untuk menghasilkan Line Chart
def generate_line_chart(data, selected_pollutant):
    st.title("Tren Keseluruhan Polusi Udara di Beijing dari Waktu ke Waktu")
    
    # Sidebar untuk memilih Polusi
    st.sidebar.title("Filter")
    selected_pollutant = st.sidebar.selectbox("Pilih Polutan", ["PM2.5", "PM10"])
    # Sidebar untuk memilih resample
    resample_type = st.sidebar.selectbox("Pilih Data", ["Day", "Month"])

    # Membuat data time series terlebih dahulu dengan mengelompokannya berdasarkan bulan atau hari
    data['date'] = pd.to_datetime(data['date'])
    if resample_type == "Day":
        data_time_series = data[['date', 'PM2.5', 'PM10']].set_index('date').resample('D').mean()
    elif resample_type == "Month":
        data_time_series = data[['date', 'PM2.5', 'PM10']].set_index('date').resample('M').mean()

    # Membuat Line Chart berdasarkan pilihan pollutant
    date_selection = st.sidebar.checkbox("Filter berdasarkan Tanggal")
    if date_selection:
        # Sidebar untuk memilih rentang tanggal
        start_date = data_time_series.index.min().to_pydatetime()
        end_date = data_time_series.index.max().to_pydatetime()
        selected_start_date = st.sidebar.date_input("Select Start Date", start_date, min_value=start_date, max_value=end_date)
        selected_end_date = st.sidebar.date_input("Select End Date", end_date, min_value=start_date, max_value=end_date)

        # Filter data berdasarkan rentang tanggal yang dipilih
        selected_start_date = pd.Timestamp(selected_start_date)
        selected_end_date = pd.Timestamp(selected_end_date)
        data_time_series = data_time_series[(data_time_series.index >= selected_start_date) & (data_time_series.index <= selected_end_date)]

    # Membuat Line Chart berdasarkan pilihan pollutant
    plt.figure(figsize=(15, 6))
    plt.plot(data_time_series.index, data_time_series[selected_pollutant], label=selected_pollutant, marker='o', linestyle='-', color='b' if selected_pollutant == 'PM2.5' else 'g')
    plt.xlabel('Tanggal')
    plt.ylabel('Konsnetrasi')
    plt.title(f'Konsentrasi Rata-rata Bulanan dari {selected_pollutant}')
    plt.legend()

    # Menambahkan garis tren untuk selected_pollutant
    x_values = np.arange(len(data_time_series))
    y_values = data_time_series[selected_pollutant]
    slope, intercept, _, _, _ = linregress(x_values, y_values)
    plt.plot(data_time_series.index, intercept + slope * x_values, linestyle='--', color='black', label=f'Trend {selected_pollutant}')

    plt.legend()
    st.pyplot(plt)
    
    # Menambahkan keterangan berbeda tergantung pada pilihan selectbox
    if selected_pollutant == "PM2.5":
        st.write("Terdapat tren penurunan yang tidak terlalu signifikan pada awal hingga akhir data PM2.5. Dan jika dilihat data tersebut dapat dikatakan mengalami kenaikan dan penurunan yang tidak beraturan atau dapat dikatakan bahwa data tersebut berfluktuasi.")     
    else:
        st.write("Terdapat tren penurunan yang signifikan pada awal hingga akhir data PM10. Dan jika dilihat data tersebut dapat dikatakan mengalami kenaikan dan penurunan yang tidak beraturan atau dapat dikatakan bahwa data tersebut berfluktuasi.")

# Fungsi untuk menghasilkan korelasi antar variabel dalam data
def korelasi(data, selected_pollutant):
    st.title("Korelasi Antar Variabel Dalam Data")
    
    # Sidebar untuk memilih Polusi
    st.sidebar.title("Filter")
    selected_pollutant = st.sidebar.selectbox("Pilih Polutan", ["PM2.5", "PM10"])
    
    # Buat subplots dengan ukuran tertentu
    fig, ax = plt.subplots(figsize=(10,6))
    # Ambil kolom yang ingin dihitung korelasinya
    pm = data[['SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', selected_pollutant]]
    # Buat mask untuk triangular heatmap
    mask = np.triu(np.ones_like(pm.corr(numeric_only=True), dtype=bool))
    # Buat heatmap
    sns.heatmap(pm.corr(numeric_only=True), annot=True, mask=mask, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
    # Atur judul
    plt.title(f"Heatmap Korelasi dari {selected_pollutant}")

    # Tampilkan plot menggunakan Streamlit
    st.pyplot(plt)
    
    # Menambahkan keterangan berbeda tergantung pada pilihan selectbox
    if selected_pollutant == "PM2.5":
        st.write("Dari plot heatmap diatas dapat dilihat bahwa variabel yang memiliki korelasi paling kuat dengan PM2.5 adalah CO (0,77) dan korelasi paling lemah adalah RAIN (-0.01). Berikut detailnya:")
        text = '''
        - **Korelasi Positif** : SO2, NO2, CO, PRES, dan DEWP.
        - **Korelasi Negatif**: O3, TEMP, RAIN, dan WSPM.
        '''
        st.write(text)  
    else:
        st.write("Dari plot heatmap diatas dapat dilihat bahwa variabel yang memiliki korelasi paling kuat dengan PM10 adalah CO (0,69) dan korelasi paling lemah adalah PRES (-0.02). Berikut detailnya:")
        text = '''
        - **Korelasi Positif** : SO2, NO2, CO, dan DEWP.
        - **Korelasi Negatif**: O3, TEMP, PRES, RAIN, dan WSPM.
        '''
        st.write(text)

# Fungsi untuk menghasilkan boxplot
def generate_vertical_bar_chart(data, selected_pollutant, data_type):
    # Sidebar untuk memilih Pollutant
    st.sidebar.title("Filter")
    selected_pollutant = st.sidebar.selectbox("Pilih Polutan", ["PM2.5", "PM10"])
    data_type =st.sidebar.selectbox("Pilih Data", ["station", "month"])
    
    st.title(f"Grafik {selected_pollutant} berdasarkan {data_type}")
    
    # Mengelompokkan berdasarkan type data dan menghitung rata-rata pollutant
    grouped_data = data.groupby(by=data_type).agg({selected_pollutant: ['mean']})
    # Reset index agar 'station' menjadi kolom biasa
    grouped_data = grouped_data.reset_index()
    # Mengurutkan DataFrame berdasarkan nilai rata-rata PM2.5 dari yang terbesar
    grouped_data = grouped_data.sort_values(by=(selected_pollutant, 'mean'), ascending=True)

    # Membuat vertical bar chart
    plt.figure(figsize=(15, 6))
    bars = plt.barh(grouped_data[data_type], grouped_data[(selected_pollutant, 'mean')])
    plt.xlabel(f'{data_type}')
    plt.ylabel(f'Rata-Rata {selected_pollutant}')
    plt.title(f'Rata-Rata {selected_pollutant} dari {data_type}')

    # Menambahkan label nilai di setiap bar
    for bar in bars:
        xval = bar.get_width()
        yval = bar.get_y() + bar.get_height() / 2
        plt.text(xval, yval, round(xval, 2), ha='left', va='center')

    # Menampilkan chart menggunakan Streamlit
    st.pyplot(plt)
    
    # Menambahkan keterangan berbeda tergantung pada pilihan selectbox
    if selected_pollutant == "PM2.5" and data_type == "station":
        st.write("Daerah yang memiliki rata rata PM2.5 terkecil adalah stasiun Dingling sebesar 67,43 sedangkan yang terbesar adalah stasiun Dongsi sebesar 86,31.") 
    elif selected_pollutant == "PM2.5" and data_type == "month":
        st.write("Rata-rata PM2.5 terkecil di bulan Agustus yaitu sebesar 53,65, sedangkan yang terbesar di bulan Desember yaitu sebesar 104,3. Hal tersebut mungkin terjadi karena bulan Agustus di china merupakan musim Panas, sedangkan bulan Desember merupakan musim dingin.")
    elif selected_pollutant == "PM10" and data_type == "station":
        st.write("Daerah yang memiliki rata rata PM10 terkecil adalah stasiun Dingling sebesar 84,22 sedangkan yang terbesar adalah stasiun Gucheng sebesar 119,33.")
    elif selected_pollutant == "PM10" and data_type == "month":
        st.write("Rata rata PM10 terkecil di bulan Agustus yaitu sebesar 71,64, sedangkan yang terbesar di bulan Maret yaitu sebesar 136,92. Hal tersebut mungkin terjadi karena bulan Agustus di china merupakan musim Panas, sedangkan bulan Maret merupakan musim dingin.")

# Sidebar
st.sidebar.title("Navigasi")
page = st.sidebar.radio("", ("Deskripsi Data", "Pola Musiman", "Pola Setiap Waktu", "Korelasi", "Lainnya"))

# Routing
if page == "Deskripsi Data":
    generate_data_description(data)
elif page == "Pola Musiman":
    generate_boxplot(data, "PM2.5")  
elif page == "Pola Setiap Waktu":
    generate_line_chart(data, "PM2.5")
elif page == "Korelasi":
    korelasi(data, "PM2.5")  
elif page == "Lainnya":
    generate_vertical_bar_chart(data, "PM2.5", "station")