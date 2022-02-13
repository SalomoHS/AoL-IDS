import streamlit as st
from multiapp import MultiApp
from apps import home, data, model # import your app modules here

app = MultiApp()
st.info('Disarankan menggununakan tampilan wide: Pilih Menu(Pojok kanan atas) - Settings - Wide Mode')
st.markdown(""" <style>
            .title{
            margin-bottom:50px;
            text-align:center;
            font-size:100px
            }
            </style>""",unsafe_allow_html=True)


st.markdown("<h2 class='title'>AOL Introduction to Data Science</h2>",unsafe_allow_html=True)

st.markdown("""
# Student Dashboard
""")


# Add all your application here
app.add_app("Dataframe Overview", home.app)
app.add_app("Descriptive Statistics", data.app)
app.add_app("Filtering", model.app)
# The main app
app.run()
