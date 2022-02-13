import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_filter = pd.read_csv("AoL_2.0.csv")

def app():
    st.title('Filtering')
    st.markdown("""<style>
                .head{
                font-size:30px;
                text-align:center;
                margin-bottom:-10px;
                }</style>""",unsafe_allow_html=True)
    with st.expander("Korelasi Antara Nilai Mata Pelajaran Satu Dengan yang Lainnya"):
        col1,col2 = st.columns([2,2])
        
        with col1:
            fig = px.scatter_matrix(df_filter,dimensions=['math score','reading score','writing score'])
            fig.update_layout(margin=dict(t=0,b=0,l=0,r=0))
            fig.update_layout(autosize=False,
                              width=600,
                              height=400)
            st.plotly_chart(fig)
        with col2:
            st.write("Semua nilai mata pelajaran siswa memiliki korelasi yang kuat di antara satu dengan yang lainnya, sehingga jika semakin tinggi nilai reading siswa maka nilai writing nya juga tinggi. begitupun juga dengan yang lainnya.")
        
    with st.expander("Latar Belakang Pendidikan Orang Tua Cukup Mempengaruhi Nilai Siswa"):
        col1,col2=st.columns([2,2])
        
        with col1:
            a = df_filter[(df_filter['parental level of education']=="high school")|(df_filter['parental level of education']=="some high school")]['Total']
            b = df_filter[(df_filter['parental level of education']=="associate's degree")|(df_filter['parental level of education']=="some college")]['Total']
            c = df_filter[(df_filter['parental level of education']=="bachelor's degree")]['Total']
            d = df_filter[(df_filter['parental level of education']=="master's degree")]['Total']

            fig = go.Figure()
            fig.add_trace(go.Scatter(name="High School", x=[1]*len(a), y=a,mode='markers',marker_color='#FFF5A5'))
            fig.add_trace(go.Scatter(name="Associate's Degree and Some College", x=[2]*len(b), y=b,mode='markers',marker_color='#FFAA64'))
            fig.add_trace(go.Scatter(name="bachelor's degree", x=[3]*len(c), y=c,mode='markers',marker_color='#FF8264'))
            fig.add_trace(go.Scatter(name="Master's Degree", x=[4]*len(d), y=d,mode='markers',marker_color='#FF6464'))
            fig.update_layout(legend_title_text='Parent Education')
            fig.update_layout(margin=dict(t=50,b=0,l=0,r=0))
            st.plotly_chart(fig)
        with col2:
            st.write("Dapat dilihat bahwa anak yang memiliki orang tua berlatar belakang pendidikan master degree memiliki nilai total terendah paling tinggi yaitu 134")
        
    with st.expander("Pengaruh Test Preparation Untuk Lulus di Mata Pelajaran Tertentu"):
        space,radio1,space2,radio2 = st.columns([1,2,1,2])
        with space:
            st.write("")
        with radio1:
            subject = st.radio(" ",("Math","Reading","Writing"))
            st.write('<style>div.row-widget.stRadio> div{flex-direction:row;}</style>',unsafe_allow_html=True)
            pelajaran = 'math score'
            stats = 'math status'
            if subject == "Math":
                pelajaran = 'math score'
                stats = 'math status'
            elif subject == "Reading":
                pelajaran = 'reading score'
                stats = 'read status'
            elif subject == "Writing":
                pelajaran = 'writing score'
                stats = 'write status'
        with space2:
            st.write("")
        with radio2:
            test = st.radio(" ",("None","Completed"))
            st.write('<style>div.row-widget.stRadio> div{flex-direction:row;}</style>',unsafe_allow_html=True)
            cek = 'none'
            preparation= 'Tidak mMengikuti'
            if test == "None":
                cek = 'none'
                preparation= 'Tidak Mengikuti'
            elif test == "Completed":
                cek = 'completed'
                preparation= 'Mengikuti'
                
        bar,sun = st.columns([2,2])
        
        with bar:
            a = df_filter[(df_filter['test preparation course']==cek)&(df_filter[pelajaran]>=75.0)]
            b = df_filter[(df_filter['test preparation course']==cek)&(df_filter[pelajaran]<75.0)]
            test = pd.concat([a,b])
            test[stats] = test[pelajaran].apply(lambda Status:'Lulus' if Status>=75 else 'Tidak Lulus')
            test['count'] = 1
            test_bar = test.groupby(by=[stats,'Class']).sum()

            index = ['Lulus']*5+['Tidak Lulus']*5
            group = ['group A','group B','group C','group D','group E']*2
            fig = px.bar(test_bar, x=index, y='count', barmode='group',color=group,height=400,text_auto=True,
                         labels={"x": subject,
                                 "count": "Jumlah Siswa",
                                 "color": "Class"})
            fig.update_layout(autosize=False,
                              width=650,
                              height=400)
            fig.update_layout(margin=dict(t=25,b=0,l=130,r=0))
            st.plotly_chart(fig)

        with sun:
            lulus = df_filter[(df_filter['test preparation course']==cek)&(df_filter[pelajaran]>=75.0)]
            lulus['count'] = 1
            lulus = lulus.sort_values(by=['Class'])
            tidak_lulus = df_filter[(df_filter['test preparation course']==cek)&(df_filter[pelajaran]<75.0)]
            tidak_lulus['count'] = 1
            tidak_lulus = tidak_lulus.sort_values(by=['Class'])
            st.write("")
            fig  = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]],subplot_titles=['Lulus','Tidak Lulus'])
            fig.add_traces(go.Pie(labels=lulus['Class'],values=lulus['count'],name='Lulus'),1,1) 
            fig.add_traces(go.Pie(labels=tidak_lulus['Class'],values=tidak_lulus['count'],name='Tidak Lulus'),1,2)
            fig.update_layout(margin=dict(t=20,b=0,l=30,r=0))
            fig.update_layout(autosize=False,
                                   width=620,
                                   height=400)
            fig.update_layout(legend_title_text='Class')
            fig.update_layout(legend=dict(orientation="h",
                                               x=0.1,
                                               y=0))
            fig.update_traces(sort=False)
            st.plotly_chart(fig)

    with st.expander("Perbandingan Total Nilai Rata-Rata Berdasarkan Gender"):
        mean_f = df_filter[df_filter['gender']=='female'].mean()
        mean_m = df_filter[df_filter['gender']=='male'].mean()
        
        mean_math = [mean_f['math score'],mean_m['math score']]
        mean_read = [mean_f['reading score'],mean_m['reading score']]
        mean_write = [mean_f['writing score'],mean_m['writing score']]
        mean_total = [mean_f['Total'],mean_m['Total']]
        
        fig = make_subplots(rows=1,cols=3,specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]], subplot_titles=['Math\n','Reading\n','Writing\n'])
        fig.add_traces(go.Pie(labels=['female','male'],values=mean_math,name='Math'),1,1)
        fig.add_traces(go.Pie(labels=['female','male'],values=mean_read,name='Reading'),1,2)
        fig.add_traces(go.Pie(labels=['female','male'],values=mean_write,name='Writing'),1,3)
            
        fig.update_layout(legend_title='Gender')
        fig.update_layout(margin=dict(t=40,b=0,l=0,r=0))
        fig.update_layout(autosize=False,
                          width=1300,
                          height=400)
        fig.update_traces(marker=dict(colors=['#FF165D','#3EC1D3']))
        st.plotly_chart(fig)
        
    with st.expander("Test Preparation Course Tidak Pengaruh dalam Kompetensi Peserta"):
        graph, exp = st.columns([2,2])
        komp = df_filter[df_filter['Status']=='Berkompeten'].groupby(by='test preparation course').count()
        t_komp =  df_filter[df_filter['Status']=='Tidak Berkompeten'].groupby(by='test preparation course').count()
        data_kompetensi = pd.concat([komp,t_komp])
        with graph:
            fig = px.bar(data_kompetensi,x=['Kompeten']*2+['Tidak Kompeten']*2,y='gender',color=['completed','none']*2,
                        color_discrete_sequence =['#3DB2FF','#FF2442'])
            fig.update_layout(xaxis_title='Status',yaxis_title='Count')
            fig.update_layout(legend=dict(title='Test',
                                          orientation='h',
                                          x=0.6,
                                          y=1.1))
            st.plotly_chart(fig)
        with exp:
            fig = make_subplots(1,2,specs=[[{'type':'domain'},{'type':'domain'}]],subplot_titles=['Kompeten','Tidak Kompeten'])
            fig.add_traces(go.Pie(labels=komp.index,values=komp['gender'],name='Kompeten'),1,1)
            fig.add_traces(go.Pie(labels=t_komp.index,values=t_komp['gender'],name='Tidak Kompeten'),1,2)
            fig.update_layout(margin=dict(t=50,b=0,l=0,r=0))
            fig.update_layout(legend_title_text='Test')
            fig.update_traces(marker=dict(colors=['#3DB2FF','#FF2442']))
            fig.update_layout(legend=dict(x=1))
            fig.update_layout(autosize=False,
                          width=620,
                          height=400)
            st.plotly_chart(fig)
            