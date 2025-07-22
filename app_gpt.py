
import streamlit as st
import openai

st.set_page_config(page_title="Controller Fénix IA", layout="centered")
st.title("🤖 Controller Fénix Inteligente")
st.write("Hola 👋 Soy tu controller financiero inteligente. Pregúntame libremente sobre facturación, clientes o costos 2025.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

CONOCIMIENTO = '''
- Facturación 2025: $76.563.813
- Materiales y pintura: 29.02% de las ventas
- Costo financiero: 4.58% de las ventas
- Último trimestre por tipo de cliente:
   - Particular: $19.039.407
   - Seguro: $20.053.234
- Último trimestre por tipo de vehículo:
   - Liviano: $11.706.036
   - Pesado: $27.386.605
'''

pregunta = st.text_input("✍️ ¿Qué quieres saber?")

if pregunta:
    with st.spinner("Pensando..."):
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un analista financiero que responde usando solo esta información:
" + CONOCIMIENTO},
                {"role": "user", "content": pregunta}
            ]
        )
        st.success(respuesta.choices[0].message["content"])
