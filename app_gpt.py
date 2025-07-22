import streamlit as st
import pandas as pd
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configura tu API Key de OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Configura acceso a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gc = gspread.authorize(credentials)

# URL o ID del Google Sheet
spreadsheet_id = "1mXxUmIQ44rd9escHOee2w0LxGs4MVNXaPrUeqj4USpk"
worksheet = gc.open_by_key(spreadsheet_id).sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Prepara contexto para GPT
contexto = f"""
Información financiera (extraída desde Google Sheets):

{df.to_string(index=False)}
"""

st.title("🤖 Fénix Automotriz - Controller IA")
st.markdown("Hola 👋 soy tu controller financiero personal. Hazme preguntas basadas en los datos disponibles.")

pregunta = st.text_input("¿Qué quieres saber?", placeholder="Ej: ¿Cuál fue la facturación del último trimestre por tipo de cliente?")

if pregunta:
    with st.spinner("Analizando datos..."):

        messages = [
            {"role": "system", "content": """Eres un analista financiero que responde usando solo esta información:
""" + contexto},
            {"role": "user", "content": pregunta}
        ]

        try:
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3
            )
            st.success(respuesta.choices[0].message["content"])

        except Exception as e:
            st.error(f"❌ Error: {e}")
