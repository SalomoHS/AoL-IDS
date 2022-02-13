import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px

df_describe = pd.read_csv("AoL_2.0.csv")
def app():
    
    st.markdown("""<style>
                    .push-up{
                    margin-up:600px;
                    }
                    .push-down{
                    margin-up:-100px;
                    }
                    .option{
                    display: inline-block;
                    }
                    </style>""",unsafe_allow_html=True)
    with st.container():
        space,curve, hist = st.columns([4,1,1])
        flag_curve = False
        flag_hist = False
        
        with space:
            st.title('Descriptive Statistics')
            
        with curve:
            st.markdown("<p class='push-up'></p>",unsafe_allow_html=True)
            Curve = st.radio("Curve",("On","Off"))
            st.write('<style>div.row-widget.stRadio> div{flex-direction:row;}</style>',unsafe_allow_html=True)
            
            if Curve == "On":
                flag_curve = True
            elif Curve == "Off":
                flag_curve = False
                
        with hist:
            st.markdown("<p class='push-up'></p>",unsafe_allow_html=True)
            Hist = st.radio("Hist",("On","Off"))
            st.write('<style>div.row-widget.stRadio> div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
            if Hist == "On":
                flag_hist = True
            elif Hist == "Off":
                flag_hist = False
    
    with st.container():
        
        describe,distplot= st.columns([2,2])
        with describe:
            st.write(df_describe.describe(),use_column_width=False)
            
        with distplot:
            columns = ['math score','reading score','writing score']
            colors = ['#A56CC1', '#A6ACEC', '#63F5EF']
            math_df_describe = df_describe[columns[0]]
            read_df_describe = df_describe[columns[1]]
            write_df_describe = df_describe[columns[2]]
            data_df_describe = [math_df_describe,read_df_describe,write_df_describe]
            dist = ff.create_distplot(data_df_describe,columns,bin_size=1,show_curve=flag_curve,show_hist=flag_hist,show_rug=False)
            dist.update_layout(autosize=False,
                               width=700,
                               height=300)
            dist.update_layout(margin=dict(t=30,b=0,l=50,r=0))
            dist.update_layout(legend=dict(orientation="h",
                                           x=0.23,
                                           y=-0.1))
            st.plotly_chart(dist)
      

        with st.container():
            space1,option,space2= st.columns([0.7,2,2])
            
            with space1:
                st.write("")
            with option:
                Score = 'math score'
                Curve = st.radio(" ",("Math","Reading","Writing","Total"))
                st.write('<style>div.row-widget.stRadio> div{flex-direction:row;}</style>',unsafe_allow_html=True)

                if Curve == "Math":
                    Score = 'math score'
                elif Curve == "Reading":
                    Score = 'reading score'
                elif Curve == "Writing":
                    Score = 'writing score'
                elif Curve == "Total":
                    Score = 'Total'
                    
            with space2:
                st.write(" ")
            
            violin,distplot= st.columns([2,2])
            with violin:
                df_describe_new = df_describe.sort_values(['Class'])
                subject_violin = px.violin(df_describe_new,x='Class',y=Score,color='gender',box=True)
                subject_violin.update_layout(margin=dict(t=30,b=0,l=0,r=50))
                subject_violin.update_layout(legend=dict(orientation="h",
                                                         x=0.37,
                                                         y=1.1))
                subject_violin.update_layout(legend_title_text='')
                dist.update_layout(margin=dict(t=30,b=0,l=0,r=0))
                st.plotly_chart(subject_violin)
                
            with distplot:
                columns = ['Total']
                colors = ['#A56CC1', '#A6ACEC', '#63F5EF']
                Total_df_describe = df_describe[columns[0]]
                data_df_describe = [Total_df_describe]
                dist = ff.create_distplot(data_df_describe,columns,bin_size=1,show_curve=flag_curve,show_hist=flag_hist,show_rug=True)
                dist.update_layout(autosize=False,
                                   width=700,
                                   height=478)
                dist.update_layout(margin=dict(t=30,b=0,l=50,r=0))
                dist.update_layout(legend=dict(orientation="h",
                                               x=0.45,
                                               y=-0.1))
                
                st.plotly_chart(dist)
