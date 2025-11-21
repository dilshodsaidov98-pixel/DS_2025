import streamlit as st
import pandas as pd 
st.title('🎈 IT')

st.write('Hello world!')

with st.expender ("DataFrame"):
  st.write('**DATA**')
  df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
  df
