import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la base de datos
def init_db():
    conn = sqlite3.connect('reservas.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS inflables (id INTEGER PRIMARY KEY, nombre TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS reservas (id INTEGER PRIMARY KEY, cliente TEXT, id_inf INTEGER, fecha DATE)')
    conn.commit()
    return conn

db = init_db()

st.title("🎈 Gestión de Inflables - Santec")

# --- Formulario de Reserva ---
with st.form("nueva_reserva"):
    st.subheader("Nueva Reserva")
    cliente = st.text_input("Nombre del Cliente")
    # Traemos los inflables de la DB para el desplegable
    inflables = pd.read_sql("SELECT * FROM inflables", db)
    opciones = {row['nombre']: row['id'] for index, row in inflables.iterrows()}
    
    seleccionado = st.selectbox("Elegí el Inflable", options=list(opciones.keys()))
    fecha = st.date_input("Fecha del evento")
    
    if st.form_submit_button("Guardar Reserva"):
        cursor = db.cursor()
        # Verificamos disponibilidad
        ocupado = cursor.execute("SELECT * FROM reservas WHERE id_inf=? AND fecha=?", (opciones[seleccionado], str(fecha))).fetchone()
        
        if ocupado:
            st.error("❌ Ese inflable ya está alquilado para esa fecha.")
        else:
            cursor.execute("INSERT INTO reservas (cliente, id_inf, fecha) VALUES (?, ?, ?)", (cliente, opciones[seleccionado], str(fecha)))
            db.commit()
            st.success("✅ ¡Reserva guardada!")

# --- Visualización de Agenda ---
st.subheader("📅 Agenda de Alquileres")
df_reservas = pd.read_sql("""
    SELECT r.fecha, c.nombre as inflable, r.cliente 
    FROM reservas r JOIN inflables c ON r.id_inf = c.id 
    ORDER BY r.fecha ASC
""", db)
st.table(df_reservas)
