import streamlit as st
import pandas as pd
import functions as fn
import plotly.express as px
mapboxToken = "insert plotly token"
@st.cache
def readCSV(name):
    return pd.read_csv(name, delimiter='|')


def main():
    st.title('Analista Inmobiliario')
    st.write("""
    Recopilación y análisis de datos inmobilarrios
        """)

    df = readCSV('DB.csv')

    ciudades = list(df['ubicacion'].unique())
    ciudades.remove('Santa Cruz de la Sierra')
    ciudades = ['Santa Cruz de la Sierra']+ciudades
    filtroCiudad = st.selectbox('CIUDAD',ciudades)
    tipoInmueble = list(df['tipoPropiedad'].unique())
    tipoInmueble.remove('Terreno')
    tipoInmueble = ['Terreno']+tipoInmueble
    filtroTipoInmueble = st.selectbox('TIPO INMUEBLE',tipoInmueble)

    #Filter Ciudad
    df = df[df['ubicacion']==filtroCiudad]
    #Filter tipoPropiedad
    df = df[df['tipoPropiedad']==filtroTipoInmueble]
    df = fn.removeOutliers(df,'USD/M2')
    #st.dataframe(df)
    #Map
    px.set_mapbox_access_token(mapboxToken)
    figMap = px.scatter_mapbox(df, lat='latitud', lon='longitud',color='USD/M2', size='USD/M2',
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=10,zoom=10,
                            #mapbox_style="carto-darkmatter"

                           )
    st.plotly_chart(figMap, use_container_width=True)

    #Distribution
    figHist = px.histogram(df, x='USD/M2',histnorm='percent')
    figHist.update_layout(title_text='DISTRIBUCION DEL VALOR DEL M²', title_x=0.5)
    figHist.update_yaxes(title_text='PORCENTAJE')
    figHist.update_xaxes(title_text='DISTRIBUCION DEL VALOR DEL M²')
    st.plotly_chart(figHist, use_container_width=True)

if __name__ == "__main__":
    main()