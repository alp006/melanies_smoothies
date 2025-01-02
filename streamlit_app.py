# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session #NEW
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie!!!  :balloon:")
st.write("""Choose **the fruit** you want in your custom Smoothie.""")

order_name = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', order_name)

cnx = st.connection("snowflake") #NEW
session = cnx.session() #NEW
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
  ingredients_string = ''
  for x in ingredients_list:
    ingredients_string += x + ' '
  #st.write(ingredients_string)

  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + order_name + """') """
  #st.write(my_insert_stmt)
  #st.stop()

  submit = st.button('Submit Order')
    
  if submit:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+order_name+'!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
