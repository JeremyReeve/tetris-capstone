import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import time
from PIL import Image
import numpy as np


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
nonfood_gdf = gdf.merge(pd.DataFrame(nonfood), left_on='Provinsi', right_on='Provinsi')



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

def define_map_non_food(non_food_gdf,year):
    # Filter GeoDataFrame based on user-selected year
    non_food_gdf = non_food_gdf[['Provinsi', year, 'geometry']]

    # Show map based on user-selected year
    fig, ax = plt.subplots(figsize=(10, 8))
    non_food_gdf.plot(column = year, cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    ax.set_xlim(95, 141)
    ax.set_ylim(-11, 6)
    ax.axis('off')

    # Display legend
    cax = fig.add_axes([0.85, 0.4, 0.03, 0.25])
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=non_food_gdf[year].min(), vmax=non_food_gdf[year].max()))
    sm.set_array([])
    fig.colorbar(sm, cax=cax)

    fig = px.choropleth(non_food_gdf, geojson=non_food_gdf.geometry,
                        locations=non_food_gdf.index, 
                        color= year, color_continuous_scale='YlOrRd', 
                        range_color=(non_food_gdf[year].min(), non_food_gdf[year].max()), 
                        labels={year:'IPM'}, hover_name='Provinsi', hover_data=[year])

    fig.update_geos(fitbounds='locations', visible=True)
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    fig.update_layout(legend_orientation='h', legend=dict(x=0, y=1.1))
    fig.update_layout(coloraxis_colorbar=dict(
        title='Persentase Pengeluaran untuk Non-Makanan pada tahun' + year,
        thicknessmode="pixels", thickness=15,
        lenmode="pixels", len=300,
        yanchor="top", y=1,
        ticks="outside", ticksuffix="%",
        dtick=5
    ))

    return fig
    



# Define Streamlit app
def main():
    st.title('Interactive Map of Provinces in Indonesia')
    st.subheader('Analisis Korelasi Persentase Rata‑Rata Pengeluaran per Kapita Sebulan Untuk Makanan dan Bukan Makanan di Daerah Perkotaan pada tahun 2017-2022 dan hubungannya dengan IPM Provinsi pada tahun 2017-2022 ')

    st.write("Melakukan analisis korelasi terhadap persentase pengeluaran untuk makanan dengan Indeks Pengembangan Manusia")
    
    st.write("Dengan hipotesis awal bahwa data akan memiliki korelasi tinggi")

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

    # display map if user click drodown
    if st.button('Show Non-Food Consumption Map '):
        st.plotly_chart(define_map_non_food(nonfood_gdf, year_str))
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


    # correlation analysis between IPM and Food Consumption
    st.subheader('Analisis Korelasi antara IPM dan Persentase Pengeluaran untuk Makanan pada tahun 2017-2022')

    image = Image.open('output.png')
    st.image(image, caption = 'Movement of IPM and Food Percentage in Indonesia', use_column_width=True)
    

    # correlation .corr for food and ipm
    # Create a list to store the IPM values for each year
    ipm_values = [70.81, 71.39, 71.92, 71.94, 72.29, 72.91]

    # Create a list to store the food percentage values for each year
    food_percentage = [46.7, 45.98, 45.9, 46.05, 45.81, 46.54]


    # Convert the lists to numpy arrays
    ipm_array = np.array(ipm_values)
    food_array = np.array(food_percentage)

    # Calculate the correlations
    correlations = np.corrcoef(ipm_array, food_array)

    abs_correlations = abs(correlations)

    st.write(f"Correlation of ipm value and food consumption percentage : {abs_correlations[0,1]}")

    st.write("Dapat dilihat bahwa korelasi data cukup rendah berikar 0.19 sehingga hipotesis awal tidak terbukti")


if __name__ == '__main__':
    main()
