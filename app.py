import streamlit as st
import pandas as pd

# CONFIGURACIÓN
SHEET_ID = "1L6DaBZJANYvnOLWvqb3GFMUTyB5A0ERUmpUY6K3h8RY"
# Este link permite que Pandas lea el sheet directamente
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.title("🎈 Reservas Mundo Inflable")

try:
    # Leer datos
    df = pd.read_csv(url)
    
    with st.form("nueva_reserva"):
        cliente = st.text_input("Nombre del cliente")
        inflable = st.selectbox("Inflable", ["3x3", "3x4", "deslizador"])
        fecha = st.date_input("Fecha")
        
        if st.form_submit_button("Verificar y Avisar"):
            # Como escribir en Google Sheets por código sin Service Account es complejo,
            # por hoy, que el script verifique disponibilidad y te dé el texto para WhatsApp.
            fecha_str = str(fecha)
            existe = df[(df['inflable'] == inflable) & (df['fecha'] == fecha_str)]
            
            if not existe.empty:
                st.error(f"❌ El {inflable} ya está ocupado el {fecha_str}")
            else:
                st.success(f"✅ ¡{inflable} disponible!")
                st.info("Anotalo manualmente en el Excel por ahora, ¡mañana configuramos la escritura pro!")

    st.subheader("📋 Agenda Actual (Desde Google Sheets)")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error al conectar: {e}")
