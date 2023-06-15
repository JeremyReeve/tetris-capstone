import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import time
from PIL import Image
import numpy as np
import seaborn as sns


plt.style.use("fivethirtyeight")

sns.set_style('whitegrid')


# Load GeoJSON data
geojson_url = 'indonesia-province-jml-penduduk.json'
gdf = gpd.read_file(geojson_url)

# Province data from local CSV file
province_data = pd.read_csv('ipm-provinsi.csv')

# output on food
food = pd.read_csv('pengeluaran_kota_makanan.csv')

#output on non-food
nonfood = pd.read_csv('pengeluaran_kota_nonmakanan.csv')


# Merge GeoDataFrame with province data
province_gdf = gdf.merge(pd.DataFrame(province_data), left_on='Provinsi', right_on='Provinsi')

# Merge again with food and nonfood data

food_gdf = gdf.merge(pd.DataFrame(food), left_on='Provinsi', right_on='Provinsi')

def define_map(province_gdf,year):
    # Filter GeoDataFrame based on user-selected year
    province_gdf = province_gdf[['Provinsi', year, 'geometry']]

    # Show map based on user-selected year
    fig, ax = plt.subplots(figsize=(10, 8))
    province_gdf.plot(column = year, cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    ax.set_xlim(95, 141)
    ax.set_ylim(-11, 6)
    ax.axis('off')

    # Display legend
    cax = fig.add_axes([0.85, 0.4, 0.03, 0.25])
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=province_gdf[year].min(), vmax=province_gdf[year].max()))
    sm.set_array([])
    fig.colorbar(sm, cax=cax)

    fig = px.choropleth(province_gdf, geojson=province_gdf.geometry,
                        locations=province_gdf.index, 
                        color= year, color_continuous_scale='YlOrRd', 
                        range_color=(province_gdf[year].min(), province_gdf[year].max()), 
                        labels={year:'IPM'}, hover_name='Provinsi', hover_data=[year])

    fig.update_geos(fitbounds='locations', visible=True)
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    fig.update_layout(legend_orientation='h', legend=dict(x=0, y=1.1))
    fig.update_layout(coloraxis_colorbar=dict(
        title='Indeks Pembangunan Manusia (IPM) tahun' + year,
        thicknessmode="pixels", thickness=15,
        lenmode="pixels", len=300,
        yanchor="top", y=1,
        ticks="outside", ticksuffix="%",
        dtick=5
    ))

    return fig

def define_map_food(food_gdf,year):
    # Filter GeoDataFrame based on user-selected year
    food_gdf = food_gdf[['Provinsi', year, 'geometry']]

    # Show map based on user-selected year
    fig, ax = plt.subplots(figsize=(10, 8))
    food_gdf.plot(column = year, cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    ax.set_xlim(95, 141)
    ax.set_ylim(-11, 6)
    ax.axis('off')

    # Display legend
    cax = fig.add_axes([0.85, 0.4, 0.03, 0.25])
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=food_gdf[year].min(), vmax=food_gdf[year].max()))
    sm.set_array([])
    fig.colorbar(sm, cax=cax)

    fig = px.choropleth(food_gdf, geojson=food_gdf.geometry,
                        locations=food_gdf.index, 
                        color= year, color_continuous_scale='YlOrRd', 
                        range_color=(food_gdf[year].min(), food_gdf[year].max()), 
                        labels={year:'IPM'}, hover_name='Provinsi', hover_data=[year])

    fig.update_geos(fitbounds='locations', visible=True)
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    fig.update_layout(legend_orientation='h', legend=dict(x=0, y=1.1))
    fig.update_layout(coloraxis_colorbar=dict(
        title='Persentase Pengeluaran untuk Makanan pada tahun' + year,
        thicknessmode="pixels", thickness=15,
        lenmode="pixels", len=300,
        yanchor="top", y=1,
        ticks="outside", ticksuffix="%",
        dtick=5
    ))

    return fig


# Define Streamlit app
def main():

    st.set_page_config(
        page_title = "Analisis Korelasi Indeks Pembangunan Manusia dengan Pengeluaran terhadap Makanan",
        layout = "wide"
    )

    st.title('Capstone Dashboard')

    with st.container():

        st.subheader('Analisis Korelasi Persentase Rata‑Rata Pengeluaran per Kapita Sebulan Untuk Makanan dan Bukan Makanan di Daerah Perkotaan pada tahun 2017-2022 dan hubungannya dengan IPM Provinsi pada tahun 2017-2022 ')
        st.write("Melakukan analisis korelasi terhadap persentase pengeluaran untuk makanan dengan Indeks Pengembangan Manusia dengan hipotesis awal bahwa kedua variabel akan memiliki korelasi tinggi")

        image = Image.open('Pasar.jpg')
        st.image(image, caption = 'Pasar sebagai tempat masyarakat membeli bahan pangan, sumber gambar: https://www.kompas.id/baca/metro/2022/10/14/judul-23')

        
        st.header("IPM dan Persentase Pengeluaran untuk Makanan di Indonesia")
        st.write("Indeks Pembangunan Manusia (IPM) dan persentase pengeluaran rumah tangga untuk makanan memiliki keterkaitan erat. IPM merupakan indikator untuk mengukur perkembangan dan kesejahteraan manusia dalam suatu negara, sedangkan persentase pengeluaran rumah tangga untuk makanan mencerminkan sejauh mana masyarakat dapat memenuhi kebutuhan pangan.")

        st.write("Tingkat pengeluaran rumah tangga untuk makanan dapat dipengaruhi oleh pendapatan yang dimiliki. Pengeluaran cenderung meningkat seiring dengan peningkatan pendapatan. Jika pola ini diikuti, peningkatan pengeluaran yang nyata sejalan dengan peningkatan pendapatan, sementara peningkatan pendapatan yang nyata berarti peningkatan kesejahteraan. Oleh karena itu, peningkatan pendapatan akan berdampak pada peningkatan IPM.")

        st.write("Keterkaitan ini menunjukkan bahwa kecukupan pendapatan berperan penting dalam tingkat pengeluaran rumah tangga untuk makanan. Ketika pendapatan meningkat, masyarakat memiliki akses yang lebih baik terhadap sumber daya ekonomi dan dapat mengalokasikan lebih banyak dana untuk memenuhi kebutuhan pangan. Namun, faktor lain seperti harga makanan, kebiasaan konsumsi, dan pola hidup juga dapat mempengaruhi persentase pengeluaran rumah tangga untuk makanan.")

        st.write("Peningkatan IPM dapat mempengaruhi pola pengeluaran rumah tangga, di mana masyarakat memiliki kemampuan ekonomi yang lebih baik untuk mengalokasikan sumber daya mereka pada hal-hal selain makanan. Pergeseran pola pengeluaran ini dapat dijadikan indikator peningkatan kesejahteraan masyarakat.")

        st.write("Dalam kesimpulannya, IPM dan persentase pengeluaran rumah tangga untuk makanan saling terkait. Pendapatan yang meningkat berpotensi meningkatkan persentase pengeluaran rumah tangga untuk makanan dan pada gilirannya meningkatkan IPM. Pola pengeluaran rumah tangga juga dapat menjadi indikator kesejahteraan masyarakat jika dana yang tersedia dialokasikan pada kebutuhan non-makanan.")


        


        col1, col2 = st.columns([3,2])

        with col1:
            st.subheader("Peta IPM dan Persentase Pengeluaran kepada Makanan Provinsi Indonesia")
            # user select year between 2017-2022
            year = st.slider('Year', 2017, 2022, 2022)

            year_str = str(year)

            # display map if user click drodown
            if st.button('Show Food Consumption Map '):
                st.plotly_chart(define_map_food(food_gdf, year_str))
                #loading screen when loading map
                with st.spinner('Loading Map...'):
                    time.sleep(5)
                    st.success('Map Loaded!')
            
            # Display map
            st.plotly_chart(define_map(province_gdf,year_str))

            #loading screen when loading map
            with st.spinner('Loading Map...'):
                time.sleep(5)
                st.success('Map Loaded!')
        with col2:
            #new line
            st.write(" ")
            st.write('\n')
            st.write(" ")

            st.write(" ")
            st.write('\n')
            st.write(" ")

            st.write(" ")
            st.write('\n')
            st.write(" ")

            st.write(" ")
            st.write('\n')
            st.write(" ")

            st.write(" ")
            st.write('\n')
            st.write(" ")

            st.subheader("Insight")

            st.write("Daerah Jawa, Kalimantan, dan Sulawesi memiliki IPM yang cukup tinggi. Hal ini menunjukkan bahwa daerah-daerah ini memiliki indikator kesejahteraan yang relatif lebih baik dibandingkan dengan daerah lainnya di Indonesia. Faktor-faktor seperti pendidikan, kesehatan, dan penghasilan masyarakat di daerah-daerah ini mungkin berkontribusi terhadap tingkat IPM yang tinggi.")
            st.write("Sebaliknya, daerah Papua dan Nusa Tenggara terlihat memiliki IPM yang rendah. Hal ini mengindikasikan bahwa daerah-daerah ini masih memiliki tantangan dalam meningkatkan kesejahteraan masyarakatnya. Perlu dilakukan upaya lebih lanjut dalam hal pendidikan, kesehatan, dan pembangunan ekonomi untuk meningkatkan IPM di daerah tersebut.")

            st.write("Persebaran persentase pengeluaran untuk makanan terlihat cukup merata di tiap pulau. Hal ini menunjukkan bahwa masyarakat di berbagai daerah memiliki pola konsumsi makanan yang relatif serupa. Meskipun terdapat perbedaan tingkat pengeluaran untuk pangan antara daerah-daerah, pola pengeluaran tersebut cenderung seragam di tiap pulau. ")


    with st.container():
        st.subheader("IPM dan Pengeluaran untuk Makanan di Indonesia berdasarkan Provinsi pada Tahun 2022")
        
        tab1, tab2 = st.tabs(["IPM", "Pengeluaran untuk Makanan"])
        
        # Province data from local CSV file
        province_data = pd.read_csv('ipm-provinsi.csv')

        # output on food
        food = pd.read_csv('pengeluaran_kota_makanan.csv')
        # set provinsi as index
        province_data = province_data.set_index('Provinsi')
        food = food.set_index('Provinsi')
        merged_2022 = pd.DataFrame()
        merged_2022['IPM'] = province_data['2022']
        merged_2022['Food'] = food['2022']
        merged_2022['Year'] = 2022
        with tab1:
            st.write("IPM berdasarkan Provinsi pada Tahun 2022")
            #display bar plot and sort the ipm in 2022, where x is the index and y is the value
            # Set the title
            
            sorted_df = merged_2022.sort_values(by='IPM')
            
            plt.figure(figsize=(20, 5))

            # Plot the bar plot
            plt.bar(sorted_df.index, sorted_df['IPM'])
            plt.xlabel('Provinsi')
            plt.ylabel('IPM')
            plt.title('IPM by Province in 2022')
            plt.xticks(rotation=90)
            st.pyplot(plt)
        with tab2:
            st.write("Pengeluaran untuk Makanan berdasarkan Provinsi pada Tahun 2022")
            #display bar plot and sort the food in 2022, where x is the index and y is the value
            sorted_df = merged_2022.sort_values(by='Food')
            
            plt.figure(figsize=(20, 5))

            # Plot the bar plot
            plt.bar(sorted_df.index, sorted_df['Food'],color = "orange")
            plt.xlabel('Provinsi')
            plt.ylabel('Food')
            plt.title('Food Consumption Percentage by Province in 2022')
            plt.xticks(rotation=90)
            st.pyplot(plt)
        
        st.subheader("Insight")
        st.write("Tingkat Indeks Pembangunan Manusia (IPM) tertinggi pada tahun 2022 terdapat di DKI Jakarta, DI Yogyakarta, dan Kalimantan Timur. Hal ini menunjukkan bahwa ketiga daerah tersebut memiliki indikator kesejahteraan yang relatif lebih tinggi dibandingkan dengan daerah lainnya di Indonesia. Faktor-faktor seperti pendidikan, kesehatan, dan penghasilan masyarakat di daerah tersebut mungkin berperan dalam menciptakan tingkat IPM yang tinggi.")
        st.write("Di sisi lain, terdapat Nusa Tenggara Barat, Sulawesi Utara, dan Kepulauan Bangka Belitung yang memiliki persentase pengeluaran untuk pangan terbesar pada tahun 2022. Hal ini mengindikasikan bahwa masyarakat di daerah-daerah tersebut mengalokasikan sebagian besar pengeluaran mereka untuk memenuhi kebutuhan pangan. Faktor-faktor seperti aksesibilitas pangan, tingkat penghasilan, dan pola konsumsi masyarakat di daerah tersebut mungkin memengaruhi persentase pengeluaran untuk pangan yang tinggi.")





    

    st.subheader("Analisis Tren IPM dan Konsumsi Makanan di Indonesia")
    # Get the column names for the years
    years = ['2017', '2018', '2019', '2020', '2021', '2022']

    # Create a list to store the IPM values for each year
    ipm_values = [70.81, 71.39, 71.92, 71.94, 72.29, 72.91]

    # Create a list to store the food percentage values for each year
    food_percentage = [46.7, 45.98, 45.9, 46.05, 45.81, 46.54]
    

    fig, ax1 = plt.subplots(figsize=(6, 4))

    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('IPM', color=color)
    ax1.plot(years, ipm_values, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Food Percentage', color=color)  # we already handled the x-label with ax1
    ax2.plot(years, food_percentage, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    st.pyplot(plt)

    st.subheader("Insight")
    st.write("Dapat dilihat bahwa IPM cenderung terus mengalami kenaikan sementara persentase pengeluaran untuk makanan cenderung  tidak memiliki pola tertentu untuk rentang waktu 2017-2022")
    st.write("IPM cenderung mengalami kenaikan seiring waktu. Hal ini menunjukkan adanya peningkatan dalam indikator pembangunan manusia di Indonesia dari tahun 2017 hingga 2022. Kenaikan IPM dapat mengindikasikan adanya peningkatan dalam aspek-aspek seperti harapan hidup, pendidikan, dan pendapatan masyarakat.")
    st.write("Persentase pengeluaran untuk makanan tidak memiliki pola tertentu seiring waktu. Meskipun IPM mengalami peningkatan secara konsisten, persentase pengeluaran untuk makanan tidak menunjukkan tren yang jelas atau pola yang konsisten selama periode tersebut. Hal ini dapat mengindikasikan adanya variasi dalam kebiasaan konsumsi makanan di masyarakat, perubahan preferensi, atau faktor-faktor ekonomi yang memengaruhi pola pengeluaran untuk makanan.")








    st.subheader("Analisis Korelasi IPM dan Konsumsi Makanan di Indonesia")
    #buat dictionary

    # output on food
    food = pd.read_csv('pengeluaran_kota_makanan.csv')
    # set provinsi as index
    province_data = pd.read_csv('ipm-provinsi.csv')
    ipm_vecctor = {}

    # set provinsi as index
    province_data = province_data.set_index('Provinsi')

    for provinsi in province_data.index:
        ipm_vecctor[provinsi] = province_data.loc[provinsi].to_numpy()

    food_vector = {}
    # set provinsi as index
    food = food.set_index('Provinsi')
    # change into zscore first
    for provinsi in food.index:
        food_vector[provinsi] = food.loc[provinsi].to_numpy()

    correlation = {}
    for provinsi in province_data.index:
        correlation[provinsi] = (np.corrcoef(ipm_vecctor[provinsi], food_vector[provinsi])[0][1])

    # dictionary to series
    correlation_series = pd.Series(correlation)

    #sort the correlation
    sorted_correlation = correlation_series.sort_values()

    tab1, tab2 = st.tabs(["Visualisasi BarChart", "Tabel Data"])

    with tab1:
        #display bar plot and sort the correlation, where x is the index and y is the value
        plt.figure(figsize=(20, 5))

        # Plot the bar plot
        plt.bar(sorted_correlation.index, sorted_correlation.values)
        plt.xlabel('Provinsi')
        plt.ylabel('Correlation')
        #also display the correlation value on top of the bar
        for i, v in enumerate(sorted_correlation.values):
            plt.text(i - 0.25, v + 0.01, str(round(v, 2)))
        plt.title('Correlation between IPM and Food Consumption Percentage by Province')
        plt.xticks(rotation=90)
        st.pyplot(plt)
    with tab2:
        correlation_series_named = correlation_series.rename('Correlation')
        st.write(correlation_series_named.to_frame())

    st.subheader("Insight")
    st.write("Provinsi-provinsi dengan IPM tertinggi seperti DKI Jakarta, DI Yogyakarta, dan Kalimantan Timur memiliki korelasi negatif. Hal ini mengindikasikan bahwa di provinsi-provinsi ini, semakin tinggi IPM, persentase pengeluaran untuk pangan cenderung lebih rendah. Kemungkinan adanya faktor-faktor lain yang memberikan kontribusi lebih besar terhadap tingkat kesejahteraan di provinsi-provinsi ini, sehingga persentase pengeluaran untuk pangan relatif lebih rendah.")
    st.write("Provinsi-provinsi dengan korelasi tinggi (>0.7 atau -0.7) adalah Sumatera Utara, Jambi, Gorontalo, Sulawesi Barat, dan Maluku. Korelasi negatif yang tinggi menunjukkan bahwa semakin tinggi IPM di provinsi-provinsi ini, persentase pengeluaran untuk pangan cenderung lebih rendah. Hal ini dapat mengindikasikan adanya kecenderungan masyarakat di provinsi-provinsi ini untuk mengalokasikan pengeluaran mereka ke sektor lain yang bukan hanya makanan.")
    st.write("Korelasi nasional yang diukur dari Indonesia sendiri adalah -0.19. Korelasi ini menunjukkan hubungan negatif yang lemah antara IPM dan persentase pengeluaran untuk pangan di tingkat nasional. Artinya, secara keseluruhan, semakin tinggi IPM di Indonesia, persentase pengeluaran untuk pangan cenderung lebih rendah. Namun, korelasi yang lemah ini menunjukkan adanya variasi yang signifikan di antara provinsi-provinsi dalam hal pola pengeluaran untuk pangan.")


    st.header("Kesimpulan")
    st.write("Hipotesis awal yang menyatakan bahwa kedua variabel akan memiliki korelasi tinggi ternyata tidak terbukti, seiring dengan hasil analisis korelasi pada tahun 2022 untuk Nasional yang hanya sebesar -0.19. Dalam grafik perkembangan IPM dan Persentase Pengeluaran untuk Makanan, tidak terlihat adanya pola yang jelas antara kedua variabel tersebut. IPM terus mengalami peningkatan seiring waktu, sementara Persentase Pengeluaran untuk Makanan tidak memiliki pola tertentu dalam rentang waktu 2017-2022. Hal ini menunjukkan bahwa hubungan antara kedua variabel tidak dapat digeneralisasi dengan korelasi yang kuat atau pola yang konsisten. Oleh karena itu, hipotesis awal perlu ditinjau ulang dan faktor-faktor lain perlu dipertimbangkan dalam analisis hubungan antara IPM dan Persentase Pengeluaran untuk Makanan.")
    st.write("Terlepas dari hipotesis yang tidak terbukti, kita mendapatkan beberapa insight sebagai berikut: ")
    st.markdown("- Provinsi-provinsi dengan IPM tertinggi seperti DKI Jakarta, DI Yogyakarta, dan Kalimantan Timur memiliki korelasi negatif dengan persentase pengeluaran untuk pangan. Hal ini menunjukkan bahwa semakin tinggi IPM suatu provinsi, semakin rendah persentase pengeluaran untuk pangan di provinsi tersebut. Kemungkinan faktor-faktor lain, seperti tingkat pendapatan dan akses terhadap sumber daya, dapat berperan dalam pola pengeluaran untuk pangan di provinsi-provinsi tersebut.")
    st.markdown("- Provinsi-provinsi dengan korelasi tinggi (lebih dari 0.7 atau -0.7) antara IPM dan persentase pengeluaran untuk pangan adalah Sumatera Utara, Jambi, Gorontalo, Sulawesi Barat, dan Maluku. Korelasi negatif yang tinggi menunjukkan bahwa semakin tinggi IPM suatu provinsi, semakin rendah persentase pengeluaran untuk pangan di provinsi tersebut. Provinsi-provinsi ini perlu diperhatikan dalam perencanaan kebijakan terkait dengan kesejahteraan masyarakat dan akses terhadap pangan yang memadai.")
    st.markdown("- Korelasi nasional di Indonesia antara IPM dan persentase pengeluaran untuk pangan pada rentang waktu 2017-2022 adalah -0.19. Korelasi yang negatif mengindikasikan adanya hubungan terbalik antara IPM dan persentase pengeluaran untuk pangan di tingkat nasional. Meskipun hubungan ini lemah, tetap penting untuk mempertimbangkan keterkaitan antara pembangunan manusia dan aspek-aspek kebutuhan pangan dalam perencanaan pembangunan yang berkelanjutan.")


if __name__ == '__main__':
    main()
