import streamlit as st
import pandas as pd
import sqlite3

from banco import criar_banco

criar_banco()

st.set_page_config(
    page_title="Sistema de Reserva de Salas",
    page_icon="🏫",
    layout="wide"
)