import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CONFIGURACIÓN
st.set_page_config(page_title="Santec Reservas", layout="centered")
url = "TU_URL_DEL_SHEET_CON_PERMISO_DE_EDITOR"

conn = st.connection("gsheets", type=GSheetsConnection)

# 1. LEER DATOS
df = conn.read(spreadsheet=url)

st.title("🎈 Gestión Santec")

with st.form("nueva_reserva", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nombre del cliente")
        inflable = st.selectbox("Inflable", ["Castillo 3x3", "Castillo 3x4", "Deslizador"])
        fecha = st.date_input("Fecha")
    with col2:
        horario = st.text_input("Horario")
        direccion = st.text_input("Dirección")
    
    if st.form_submit_button("Confirmar Reserva"):
        # Lógica de stock
        fecha_str = str(fecha)
        ocupados = len(df[(df['inflable'] == inflable) & (df['fecha'] == fecha_str)])
        max_stock = 2 if inflable == "Castillo 3x3" else 1
        
        if ocupados >= max_stock:
            st.error(f"❌ No hay stock de {inflable}")
        elif not cliente:
            st.warning("Poné el nombre del cliente")
        else:
            # AGREGAR FILA
            nueva_fila = pd.DataFrame([{
                "cliente": cliente, "inflable": inflable, 
                "fecha": fecha_str, "horario": horario, "direccion": direccion
            }])
            df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
            conn.update(spreadsheet=url, data=df_actualizado)
            st.success("✅ ¡Anotado!")
            st.rerun()

st.subheader("📋 Próximas Reservas")
st.dataframe(df, use_container_width=True)
