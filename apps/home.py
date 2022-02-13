import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
st.set_page_config(page_title="Student Visualization Dashboard",
                   layout='wide')
df = pd.read_csv("AoL_2.0.csv")

gender = df.copy()
gender = gender.groupby(['gender']).agg({'gender':'count'})

pendidikan_ortu = df.copy()
pendidikan_ortu=pendidikan_ortu.groupby(by="parental level of education").agg({'parental level of education':'count'})

group = df.copy()
group = group.groupby(by='Class').count()

def app():
    st.markdown('''
            <style>
            .margin{
            margin-top:65px;
            }
            .head{
            font-size:30px;
            text-weigth=bold;
            text-align:center;
            margin-top:120px;
            }
            .describe-p1{
            font-size:30px;
            text-weigth=bold;
            text-align:center;
            margin-top:95px;
            margin-bottom:-5px;
            }
            .describe-p2{
            text-align:center;
            font-size:50px !important;
            font-family: 'Varela Round';
            }
            .describe-span{
            text-align:center;
            font-size:50px !important;
            font-family: 'Varela Round';
            }
            .big-font{
            font-size:100px !important;
            font-family: 'Varela Round';
            text-align:center;
            margin-top:-15px;
            }
            </style>''',
            unsafe_allow_html=True)
    st.title('Dataframe Overview')
    
    
    with st.container():
        dataframe, describe = st.columns([2,2])
        
        with dataframe:
            st.dataframe(df)
        with describe:
            st.markdown("<p class='describe-p1'>Number of rows and columns</p>",unsafe_allow_html=True)
            st.markdown(f"<p class='describe-p2'>{df.shape[0]} <span class='head'>rows</span> x {df.shape[1]} <span class='head'>columns</span></p>",unsafe_allow_html=True)
        

    with st.container():
        info, PieChart, BarChart = st.columns([2,2.5,3])
    
        with info:
            st.markdown("<p class='head'>Total Students</p>",unsafe_allow_html=True)
            count=df['gender'].count()
            st.markdown(f"<p class='big-font'>{count:,}</p>",unsafe_allow_html=True)

        with PieChart:
            gender_df = gender.T
            pie_jml_org = px.pie(gender,
                                 hole=.3,
                                 values='gender',
                                 names=gender_df.columns,
                                 color=gender_df.columns,
                                 color_discrete_map={"female":"EF2F88",
                                                    "male":"8843F2"})
            pie_jml_org.update_layout(margin=dict(t=0, b=0, l=5, r=1))
            pie_jml_org.update_layout(legend_font_size=19)
            pie_jml_org.update_layout(legend=dict(y=0.80))
            st.plotly_chart(pie_jml_org,use_container_width=True)

        with BarChart:
            gender_df = gender.rename(index={'female':'Female','male':'Male'})
            gender_df = gender.rename(columns={'gender':'Count'})

            bar_jml_org = px.bar(gender_df,
                                 y=gender_df.index,
                                 x='Count',
                                 color=gender_df.index,
                                 color_discrete_sequence =['#EF2F88','#8843F2'],
                                 height=300,
                                 text_auto=True,
                                orientation='h')
            bar_jml_org.update_layout(legend_title_text='Gender',legend_font_size=15,yaxis_visible=False, yaxis_showticklabels=False)
            bar_jml_org.update_layout(legend=dict(orientation="h",
                                          yanchor="bottom",
                                          y=1.02,
                                          xanchor="right",
                                          x=1))
            bar_jml_org.update_xaxes(title_font=dict(size=20))
            bar_jml_org.update_traces(textposition='inside', textfont_size=15)
            st.markdown("<p class='margin'></p>",unsafe_allow_html=True)
            st.plotly_chart(bar_jml_org,use_container_width=True)
        
    st.markdown('---')
    #=========================SECOND CONTAINER======================
    with st.container():
        info, PieChart, BarChart = st.columns([2,2.5,3])

        with info:
            st.markdown("<p class='head'>Total Groups</p>",unsafe_allow_html=True)
            count=0
            for i in group.index:
                count+=1
            st.markdown(f"<p class='big-font'>{count}</p>",unsafe_allow_html=True)

        with PieChart:
            pie_group = px.pie(group,
                               hole=0.3,
                               names=group.index,
                               values='gender',
                               color=group.index)
            pie_group.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            pie_group.update_layout(legend=dict(y=0.85))
            pie_group.update_traces(sort=False, selector=dict(type='pie'))
            st.plotly_chart(pie_group,use_container_width=True)

        with BarChart:
            kelompok = group.rename(columns={'gender':'Count'})
            bar_grou = px.bar(kelompok,
                               y='Count',
                               x=kelompok.index,
                               color=kelompok.index,
                               height=450,
                               text_auto=True)
            bar_grou.update_layout(legend_title_text='Group',yaxis_visible=True, yaxis_showticklabels=True)
            bar_grou.update_xaxes(title_font=dict(size=20))
            bar_grou.update_traces(textposition='inside', textfont_size=15)
            st.plotly_chart(bar_grou,use_container_width=True)

    st.markdown('---')

    #========================THIRD CONTAINER=====================
    with st.container():
        info, PieChart, BarChart = st.columns([2,2.5,3])

        with info:
            st.markdown("<p class='head'>Parent Education</p>",unsafe_allow_html=True)
            count=0;
            for i in pendidikan_ortu.index:
                count+=1
            st.markdown(f"<p class='big-font'>{count}</p>",unsafe_allow_html=True)
        with PieChart:
            pie_pendidikan=px.pie(pendidikan_ortu,
                             hole=0.3,
                             names=pendidikan_ortu.index,
                             values='parental level of education',
                             color=pendidikan_ortu.index)
            pie_pendidikan.update_traces(sort=False, selector=dict(type='pie'))
            pie_pendidikan.update_layout(margin=dict(t=0,b=0,l=0,r=0))
            pie_pendidikan.update_layout(legend=dict(x=1,
                                                y=0.99))
            st.plotly_chart(pie_pendidikan,use_container_width=True)

        with BarChart:
            pendidikan = pendidikan_ortu.rename(columns={'gender':'Count'})
            bar_pendidikan=px.bar(pendidikan_ortu,
                                 x=pendidikan_ortu.index,
                                 y='parental level of education',
                                 color=pendidikan_ortu.index,
                                 height=450,
                                 text_auto=True,
                                 labels={"index":"Eduation"})
            bar_pendidikan.update_layout(legend_title_text='Education')
            bar_pendidikan.update_xaxes(title_font=dict(size=20))
            st.plotly_chart(bar_pendidikan,use_container_width=True)
