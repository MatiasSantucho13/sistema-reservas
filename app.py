import streamlit as st
import pandas as pd

# CONFIGURACIÓN
SHEET_ID = "1L6DaBZJANYvnOLWvqb3GFMUTyB5A0ERUmpUY6K3h8RY"
URL_LECTURA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
URL_FORMULARIO = "PEGÁ_ACÁ_EL_LINK_DE_TU_GOOGLE_FORM"

st.set_page_config(page_title="Santec Inflables", layout="centered")
st.title("🎈 Gestión de Reservas")

# 1. BOTÓN PARA ANOTAR (Esto no falla nunca)
st.link_button("➕ REGISTRAR NUEVA RESERVA", URL_FORMULARIO, use_container_width=True)

st.divider()

# 2. VER AGENDA (Lectura en tiempo real)
try:
    df = pd.read_csv(URL_LECTURA)
    st.subheader("📅 Próximas Reservas")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error("Conectando con la base de datos...")
