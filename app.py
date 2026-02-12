import streamlit as st
import pandas as pd
import requests

# CONFIGURACIÓN
SHEET_ID = "1L6DaBZJANYvnOLWvqb3GFMUTyB5A0ERUmpUY6K3h8RY"
URL_LECTURA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
URL_ESCRITURA = "https://script.google.com/macros/s/AKfycbyqGi6N5CJsIIaKTbJVVct5vfkVBC65qj3I0sAX9BoRMB8ujHP3sQBYr1AiXARq_VaT/exec" 

st.title("🎈 Gestión Santec")

try:
    # 1. LECTURA (Vía Pandas directo)
    df = pd.read_csv(URL_LECTURA)
    
    with st.form("registro", clear_on_submit=True):
        cliente = st.text_input("Cliente")
        inflable = st.selectbox("Inflable", ["Castillo 3x3", "Castillo 3x4", "Deslizador"])
        fecha = st.date_input("Fecha")
        horario = st.text_input("Horario")
        direccion = st.text_input("Dirección")
        
        if st.form_submit_button("Confirmar"):
            # Lógica de stock doble para el 3x3
            fecha_str = str(fecha)
            ocupados = len(df[(df['inflable'] == inflable) & (df['fecha'] == fecha_str)])
            max_stock = 2 if inflable == "Castillo 3x3" else 1
            
            if ocupados >= max_stock:
                st.error(f"❌ Sin stock para {inflable}")
            else:
                # ENVIAR DATOS
                res = requests.post(URL_ESCRITURA, json={
                    "cliente": cliente, "inflable": inflable, 
                    "fecha": fecha_str, "horario": horario, "direccion": direccion
                })
                if res.status_code == 200:
                    st.success("✅ ¡Anotado!")
                    st.rerun()

    st.subheader("📅 Agenda")
    st.dataframe(df.sort_values(by="fecha"))

except Exception as e:
    st.error(f"Error: {e}")
