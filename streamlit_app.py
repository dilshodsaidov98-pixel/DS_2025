import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

st.title('🤖 MY FIRST PROJECT')

st.write('Lets do it!')

with st.expander("DATA"):
  st.write('**OUR DATA**')
  df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
  df

with st.expander("Visualization"):
  st.scatter_chart(data=df, x='bill_length_mm', y='body_mass_g', color='species')

X_raw = df.drop('species', axis=1)
y_raw = df.species

with st.sidebar:
  st.header('Input features')
  island = st.selectbox('**Island**', ('Torgersen', 'Dream', 'Biscoe'))
  bill_length_mm = st.slider("**bill_length_mm**", 32.1, 59.6, 34.1)
  bill_depth_mm = st.slider("**bill_depth_mm**", 32.1, 59.6, 45.1)
  flipper_length_mm = st.slider("**flipper_length_mm**", 32.1, 59.6, 55.1)
  body_mass_g = st.slider("**body_mass_g**", 2700, 6300, 4207)
  sex = st.selectbox('**Gender**', ('male', 'female'))

data = {'island':island,
        'bill_length_mm':bill_length_mm,
        'bill_depth_mm':bill_depth_mm,
        'flipper_length_mm':flipper_length_mm,
        'body_mass_g':body_mass_g,
        'sex':sex}
input_df = pd.DataFrame(data, index=[0])
input_penguins = pd.concat([input_df, X_raw], axis=0)

with st.expander('Input features'):
  st.write("**Input raw**")
  input_df

encode = ['island', 'sex']
df_penguins = pd.get_dummies(input_penguins, prefix=encode)

target_mapper = {'Adelie':0,
                'Gentoo':1,
                'Chinstrap':2}

def target_encode(val):
  return target_mapper[val]

# Split on train and input
y = y_raw.apply(target_encode)
X = df_penguins[1:]

input_raw = df_penguins[:1]
with st.expander('Data preparation'):
  st.write("**Encoded X**")
  input_raw

# Model training
clf = RandomForestClassifier()
clf.fit(X, y)

# Apply model for input_df
prediction = clf.predict(input_raw)
prediction_proba = clf.predict_proba(input_raw)

df_prediction = pd.DataFrame(prediction_proba)
df_prediction.columns = ['Adelie', 'Gentoo', 'Chinstrap']
df_prediction.rename(columns = {0: 'Adelie',
                               1:'Gentoo',
                               2:'Chinstrap'})

# Display prediction
st.subheader("Predictied penguins")
st.dataframe(df_prediction,
            column_config={
              'Adelie':st.column_config.ProgressColumn(
                'Adelie',
                format = '%f',
                width = 'medium',
                min_value=0,
                max_value=1
              ),
              'Gentoo':st.column_config.ProgressColumn(
                'Gentoo',
                format = '%f',
                width = 'medium',
                min_value=0,
                max_value=1
              ),
              'Chinstrap':st.column_config.ProgressColumn(
                'Chinstrap',
                format = '%f',
                width = 'medium',
                min_value=0,
                max_value=1
              ),
            }, hide_index=True)

penguins_species = np.array(['Adelie', 'Gentoo', 'Chinstrap'])
st.success(str(penguins_species[prediction[0]]))
