import streamlit as st


pg = st.navigation([st.Page('dashboard.py',title='Dashboard'),st.Page('windlogger.py',title='Dados por Aerogerador'),st.Page('curvas.py', title='Curvas de potência')])

pg.run()






