import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Gestión de Inflables", layout="centered")

# --- INTERFAZ ---
st.title("🎈 Reservas Santec")
url = "https://docs.google.com/spreadsheets/d/1L6DaBZJANYvnOLWvqb3GFMUTyB5A0ERUmpUY6K3h8RY/edit?gid=1579374829#gid=1579374829"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url)
except:
    st.error("Error de conexión. Revisá que el Sheet sea público para editar.")
    st.stop()

with st.form("nueva_reserva"):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nombre del cliente")
        inflable = st.selectbox("Inflable", ["Castillo 3x3", "Tobogán Gigante", "Cancha Jabonosa"])
    with col2:
        fecha = st.date_input("Fecha del evento")
    
    if st.form_submit_button("Confirmar Reserva"):
        # Validación: evitar duplicados
        fecha_str = str(fecha)
        existe = df[(df['inflable'] == inflable) & (df['fecha'] == fecha_str)]
        
        if not existe.empty:
            st.error(f"Ese inflable ya está ocupado el {fecha_str}")
        else:
            nueva_fila = pd.DataFrame([{"cliente": cliente, "inflable": inflable, "fecha": fecha_str}])
            df_final = pd.concat([df, nueva_fila], ignore_index=True)
            conn.update(spreadsheet=url, data=df_final)
            st.success("¡Reserva guardada!")
            st.balloons()

st.subheader("📋 Agenda Actual")
st.dataframe(df, use_container_width=True)


https://docs.google.com/spreadsheets/d/1L6DaBZJANYvnOLWvqb3GFMUTyB5A0ERUmpUY6K3h8RY/edit?usp=sharing
