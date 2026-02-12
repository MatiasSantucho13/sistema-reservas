import streamlit as st
import pandas as pd
import requests

# CONFIGURACIÓN
SHEET_ID = "1L6DaBZJANYvnOLWvqb3GFMUTyB5A0ERUmpUY6K3h8RY"
URL_LECTURA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
URL_ESCRITURA = "https://script.google.com/macros/s/AKfycbyqGi6N5CJsIIaKTbJVVct5vfkVBC65qj3I0sAX9BoRMB8ujHP3sQBYr1AiXARq_VaT/exec" 

st.title("🎈 Reservas Inflables")

try:
    # 1. LECTURA (Vía Pandas directo)
    df = pd.read_csv(URL_LECTURA)
    
    with st.form("registro", clear_on_submit=True):
        cliente = st.text_input("Cliente")
        inflable = st.selectbox("Inflable", ["Castillo 3x3", "Castillo 3x4", "Deslizador"])
        fecha = st.date_input("Fecha")
        horario = st.text_input("Horario")
        direccion = st.text_input("Dirección")
        
if st.form_submit_button("Confirmar Reserva"):
            # 1. Normalizar la fecha para comparar
            fecha_str = str(fecha)
            
            # 2. Contar cuántos de ese inflable hay ese día
            # Usamos una máscara para filtrar el DataFrame
            reservas_dia = df[(df['inflable'] == inflable) & (df['fecha'] == fecha_str)]
            cantidad_ocupada = len(reservas_dia)
            
            # 3. Definir stock máximo
            # Si es 3x3 permitimos 2, para el resto solo 1
            stock_maximo = 2 if inflable == "Castillo 3x3" else 1
            
            if cantidad_ocupada >= stock_maximo:
                st.error(f"❌ ¡Sin stock! Ya hay {cantidad_ocupada} reservado(s) para el {fecha_str}.")
            elif not cliente or not horario:
                st.warning("⚠️ Por favor, completá al menos el nombre y el horario.")
            else:
                # 4. ENVIAR DATOS (Solo si pasó el control de stock)
                try:
                    res = requests.post(URL_ESCRITURA, json={
                        "cliente": cliente, 
                        "inflable": inflable, 
                        "fecha": fecha_str, 
                        "horario": horario, 
                        "direccion": direccion
                    })
                    if res.status_code == 200:
                        st.success(f"✅ ¡Reserva confirmada! ({inflable} unidad {cantidad_ocupada + 1})")
                        st.balloons()
                        # Forzamos recarga para ver la nueva fila en la tabla
                        st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
