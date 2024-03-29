import streamlit
import pandas
import snowflake.connector
import requests


streamlit.title('My Parents My healthy diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()



#my_cur.execute("insert into fruit_load_list values ('from streamlit')" )

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
    return "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like information about?')
if streamlit.button('Add fruit'):
  streamlit.write(insert_row_snowflake(add_my_fruit))

if streamlit.button('Get Fruit list'):
  my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
  my_data_rows = my_cur.fetchall()
  streamlit.header("The fruit load list contains:")
  streamlit.dataframe(my_data_rows)
    


