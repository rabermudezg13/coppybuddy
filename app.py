import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Bullhorn Buddy", layout="centered")

st.title("📇 Bullhorn Buddy")
st.caption("Avanza contacto por contacto, limpia y pega con estilo ☕")

uploaded_file = st.file_uploader("📎 Sube tu archivo CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, usecols=['name', 'email', 'phone'])

    # Limpiar teléfonos
    def limpiar(phone):
        phone = re.sub(r'\D', '', str(phone))
        if len(phone) == 10:
            return '+1' + phone
        elif len(phone) > 10 and phone.startswith('1'):
            return '+' + phone
        elif len(phone) > 10:
            return '+1' + phone[-10:]
        return f'Número inválido ({phone})'

    df['phone'] = df['phone'].apply(limpiar)

    st.session_state['index'] = st.session_state.get('index', 0)

    if st.session_state['index'] < len(df):
        contacto = df.iloc[st.session_state['index']]
        st.subheader(f"👤 Contacto #{st.session_state['index'] + 1}")

        col1, col2 = st.columns([1, 3])
        col1.markdown("**Nombre:**")
        col2.code(contacto['name'], language='')

        col1.markdown("**Email:**")
        col2.code(contacto['email'], language='')

        col1.markdown("**Teléfono:**")
        col2.code(contacto['phone'], language='')

        if st.button("➡️ Siguiente contacto"):
            st.session_state['index'] += 1
    else:
        st.success("🎉 Todos los contactos han sido revisados.")
        if st.button("🔁 Reiniciar"):
            st.session_state['index'] = 0
