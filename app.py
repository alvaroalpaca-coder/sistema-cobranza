import streamlit as st
import pandas as pd
from twilio.rest import Client
import time
import os

# Configuración de la página
st.set_page_config(page_title="Sistema de Cobranza WhatsApp", layout="centered")
st.title("📲 Sistema de Cobranza - Envio de Msj por WhatsApp")

# Credenciales (Mantén las tuyas aquí)
ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Interfaz de usuario
st.info("Sube tu archivo Excel con las columnas 'NOMBRE' y 'TELEFONO'.")
archivo_subido = st.file_uploader("Selecciona el archivo Excel", type=["xlsx"])

if archivo_subido is not None:
    df = pd.read_excel(archivo_subido)
    st.write("Vista previa de la base de datos:")
    st.dataframe(df.head()) # Muestra las primeras filas

    if st.button("🚀 Iniciar Envío Masivo"):
        progreso = st.progress(0)
        status_text = st.empty()
        
        for index, fila in df.iterrows():
            nombre = str(fila['NOMBRE'])
            telefono = f"whatsapp:+{str(int(fila['TELEFONO']))}"
            
            try:
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=f"Hola {nombre}, este es un recordatorio de pago.",
                    to=telefono
                )
                st.success(f"Enviado a {nombre}")
            except Exception as e:
                st.error(f"Error con {nombre}: {e}")
            
            # Actualizar barra de progreso
            progreso.progress((index + 1) / len(df))
            time.sleep(0.5)
        
        st.balloons() # ¡Efecto de celebración al terminar!
        st.success("¡Proceso completado con éxito!")
