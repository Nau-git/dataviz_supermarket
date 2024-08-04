import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import io
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Myanmar Supermarket Dashboard",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://bit.ly/naufal-git',
        'Report a bug': "https://bit.ly/naufal-linkedin",
        'About': """This webapp is made as one of the assignments in Hacktiv8 Full Time Data Science program. 
        It is created to fulfill the Milestones 1 project in the phase 0 of the program.""",
    }
)

st.title('Myanmar Supermarket Info Page')
st.image('header.jpg')


@st.cache_data
def load_data():
    data = pd.read_csv('supermarket_sales_cleaned.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data
df=load_data()
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()



pages = st.sidebar.selectbox("Page selection :", ['Homepage', "Hypothesis Testing", "Data Visualization"])
if pages == 'Homepage':       ############################## Homepage ########################
    st.header('Homepage')
    
    st.write('This is the homepage of the web app. Here you can see the brief overview of the dataset.')
    st.subheader('Dataset')
    with st.expander("Show dataset"):
        st.write(df.head())
    with st.expander("See explanation"):
        st.write('The dataset is a historical sales data of a supermarket company in Myanmar. The data was recorded in 3 different branches for 3 months.')
        st.write('The columns are self-explanatory.')
        st.write('\'cogs\' is calculated from Quantity x Unit price, and \'Total\' is from cogs + Tax 5%')
    st.subheader('The dataset has no missing value.')
    with st.expander("See info table"):
        st.text(s)

elif pages == 'Hypothesis Testing':   ### Hypothesis Testing page
    st.header("Hypothesis Testing Page")
    
    ####################################### Hypothesis testing 1 #######################################
    with st.expander("Hypothesis Testing #1"):
        st.subheader('Hypothesis Testing #1')
        st.write(df.groupby('Gender')['Rating'].mean())
        st.text('''         Table above shows the average rating given by male and female customers to the 
        supermarket. From here, one can have the idea to question whether male 
        customers give better rating than female customers, or vice versa.''')
        st.text(''' Hypothesis statement:
                    * H0: μFemaleRating = μMaleRating
                    * H1: μFemaleRating != μMaleRating
        ''')
        st.text('Hypothesis testing using 2 tailed t-test for 2 samples:')
        female = df[(df['Gender']=='Female')]
        male = df[(df['Gender']=='Male')]
        t_stat, p_val = stats.ttest_ind(female['Rating'], male['Rating'])
        st.write('P-value: ', p_val)
        #st.write('t-statistics: ', t_stat)
        ####### the distribution ########
        female_pop = np.random.normal(female['Rating'].mean(),female['Rating'].std(),10000)
        male_pop = np.random.normal(male['Rating'].mean(),male['Rating'].std(),10000)

        # confidence interval based on female
        # choose cv = 0.05 -> since 2 tailed, we use 0.95 as it is. 
        ci = stats.norm.interval(0.95, female['Rating'].mean(), female['Rating'].std())

        fig = plt.figure(figsize=(20,5))
        sns.histplot(female_pop, label='female Rating Stats *Pop',color='blue', kde=True)
        sns.histplot(male_pop, label='male Rating Stats *Pop',color='red', kde=True)
        # mean
        plt.axvline(female['Rating'].mean(), color='blue', linewidth=2, label='female Rating mean')
        plt.axvline(male['Rating'].mean(), color='red',  linewidth=2, label='male Rating mean')
        plt.axvline(ci[1], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
        plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
        # alternative hypotesis
        plt.axvline(female_pop.mean()+t_stat*female_pop.std(), color='black', linestyle='dashed', linewidth=2, label = 'Alternative Hypothesis')
        plt.axvline(female_pop.mean()-t_stat*female_pop.std(), color='black', linestyle='dashed', linewidth=2)
        plt.legend()
        print(ci[0])
        st.pyplot(fig)
        st.text('''         P-value is above the \u03B1 (0.05). 
        Black dashed-line (the alternative hypothesis) is located inside of the confidence 
        interval. 
        We fail to reject H0 (μFemaleRating = μMaleRating). 
        In another word, the average rating from female and male customers are not significantly 
        different.
        ''')
    ###################### end of hypothesis testing 1 #####################

    ####################################### Hypothesis testing 2 #######################################
    with st.expander("Hypothesis Testing #2"):
        st.subheader('Hypothesis Testing #2')
        st.write(df.groupby('City')['gross income'].mean())
        st.text('''         Above table shows the average gross income of each city. Given this information, 
        one can question which city has highest gross income. 
        Or did every city generate the same gross income?''')
        st.text(''' Hypothesis statement:
                * H0 : μMandalay = μNaypyitaw = μYangon
                * H1 : μMandalay != μNaypyitaw != μYangon
        ''')
        st.text('Hypothesis testing using ANOVA:')
        man = df[(df['City']=='Mandalay')]['gross income']
        nay = df[(df['City']=='Naypyitaw')]['gross income']
        yan = df[(df['City']=='Yangon')]['gross income']
        gross_man = df[(df['City']=='Mandalay')]
        gross_nay = df[(df['City']=='Naypyitaw')]
        gross_yan = df[(df['City']=='Yangon')]
        f_stat, p_value = stats.f_oneway(man, nay, yan)
        st.write('P-value: ', p_value)
    ########## the distribution ###########
        mandalay_pop = np.random.normal(gross_man['gross income'].mean(),gross_man['gross income'].std(),10000)
        naypyitaw_pop = np.random.normal(gross_nay['gross income'].mean(),gross_nay['gross income'].std(),10000)
        yangon_pop = np.random.normal(gross_nay['gross income'].mean(),gross_yan['gross income'].std(),10000)

    # confidence interval based on gross_man
    # choose cv = 0.05 -> since 2 tailed, we use 0.95 as it is. 
        ci = stats.norm.interval(0.95, gross_man['gross income'].mean(), gross_man['gross income'].std())

        fig = plt.figure(figsize=(20,5))
        sns.histplot(mandalay_pop, label='mandalay gross income Stats *Pop',color='blue', kde=True)
        sns.histplot(naypyitaw_pop, label='naypyitaw gross income Stats *Pop',color='red', kde=True)
        sns.histplot(yangon_pop, label='yangon gross income Stats *Pop',color='yellow', kde=True)
    # mean
        plt.axvline(gross_man['gross income'].mean(), color='blue', linewidth=2, label='mandalay gross income mean')
        plt.axvline(gross_nay['gross income'].mean(), color='red',  linewidth=2, label='naypyitaw gross income mean')
        plt.axvline(gross_yan['gross income'].mean(), color='yellow',  linewidth=2, label='yangon gross income mean')
        plt.axvline(ci[1], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
        plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
    # alternative hypotesis
        plt.axvline(mandalay_pop.mean()+t_stat*mandalay_pop.std(), color='black', linestyle='dashed', linewidth=2, label = 'Alternative Hypothesis')
        plt.axvline(mandalay_pop.mean()-t_stat*mandalay_pop.std(), color='black', linestyle='dashed', linewidth=2)
        plt.legend()
        print(ci[0])
        st.pyplot(fig)
        st.text('''         P-value is above \u03B1. 
        We fail to reject H0 (μMandalay = μNaypyitaw = μYangon). 
        The alternative hypothesis (black dashed-line) is located inside of the confidence 
        interval.
        In another word, the average gross income is not significantly different among the 
        three cities.
        ''')

    # New feature: Correlation Analysis
    with st.expander("Correlation Analysis"):
        st.subheader('Correlation Heatmap')
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
        fig.update_layout(title="Correlation Heatmap of Numeric Variables")
        st.plotly_chart(fig)
        st.write("This heatmap shows the correlation between numeric variables in the dataset.")

else:   ##################################### Data Viz page ##########################
    st.header('Data Visualization Page')
    
    ############ Chart #1 ############
    with st.expander('Product line'):
        st.subheader('Product line')
        #st.write('Barplot of the product line using Seaborn')
        fig = plt.figure(figsize=(6,3))
        bar = sns.countplot(x='Product line', data=df,)
        bar.set_xticklabels(bar.get_xticklabels(),rotation = 30)
        st.pyplot(fig)
        st.write("""
            The figure above shows the product count for each product line listed in the dataset. As we can see, the highest count is held by Fashion accessories and then 
            followed by Food and beverages by a slim margin.            
        """)
        select_product = st.selectbox('Select a product line to see the number of count', options=df['Product line'].unique(), index=5)
        number_of_product_line = df['Product line'].value_counts()
        if select_product == 'Fashion accessories':
            a = number_of_product_line[0]
            st.write(f'There are {a} of {select_product} counted in the dataset.')
        elif select_product == 'Food and beverages':
            b = number_of_product_line[1]
            st.write(f'There are {b} of {select_product} counted in the dataset.')
        elif select_product == 'Electronic accessories':
            c = number_of_product_line[2]
            st.write(f'There are {c} of {select_product} counted in the dataset.')
        elif select_product == 'Sports and travel':
            d = number_of_product_line[3]
            st.write(f'There are {d} of {select_product} counted in the dataset.')
        elif select_product == 'Home and lifestyle':
            e = number_of_product_line[4]
            st.write(f'There are {e} of {select_product} counted in the dataset.')
        elif select_product == 'Health and beauty':
            f = number_of_product_line[5]
            st.write(f'There are {f} of {select_product} counted in the dataset.')
    
    ######### Chart #2 #########
    with st.expander('Stat per branch'):
        st.subheader('Stat per branch')
        select_col = st.selectbox('Select an attribute to see the stat per branch', options=('Total', 'cogs', 'gross income', 'Rating', 'gross margin percentage', 'Quantity', 'Tax 5%'), index=0)
        fig1, ax1 = plt.subplots(figsize=(5,3))
        sns.barplot(x=df['Branch'], y=df[select_col], order=['A', 'B', 'C'])
        st.pyplot(fig1)

    ########### Chart #3 ###########
    with st.expander('Stat per branch in a pie chart'):
        st.subheader('Stat per branch in a pie chart')
        select_att = st.selectbox('Select an attribute to see the stat in pie chart', options=('Total', 'cogs', 'gross income', 'gross margin percentage', 'Quantity', 'Tax 5%'), index=0)
        fig4 = px.pie(df, values=select_att, names='Branch', title=f'Sum of {select_att} per branch', hole=.3)
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        fig4.update_layout(uniformtext_minsize=18, uniformtext_mode='hide')
        st.plotly_chart(fig4)
        st.write("""
            The dataset is clearly fabricated rather "lazily". The percentage of each branch is almost the same for all the attributes.
            Another possibility is that the dataset contributor is purposely trying to make the dataset as easy to read as possible.             
        """)

    # Improved Chart #4: Time series with multiple metrics
    with st.expander('Multi-metric Time Series'):
        st.subheader('Multi-metric Time Series')
        metrics = st.multiselect('Select metrics to display', 
                                 options=['Quantity', 'Total', 'cogs', 'gross income', 'Rating'],
                                 default=['Quantity', 'Total'])
        
        fig = make_subplots(rows=len(metrics), cols=1, shared_xaxes=True, 
                            vertical_spacing=0.05, subplot_titles=metrics)
        
        for i, metric in enumerate(metrics, 1):
            for branch in df['Branch'].unique():
                branch_data = df[df['Branch'] == branch]
                fig.add_trace(
                    go.Scatter(x=branch_data['Date'], y=branch_data[metric], 
                               mode='lines', name=f'{branch} - {metric}'),
                    row=i, col=1
                )
        
        fig.update_layout(height=300*len(metrics), title_text="Time Series of Multiple Metrics by Branch")
        fig.update_xaxes(rangeslider_visible=True, row=len(metrics), col=1)
        st.plotly_chart(fig)
        st.write("Use the range slider at the bottom to zoom in on specific date ranges.")

    # New feature: Customer Segment Analysis
    with st.expander('Customer Segment Analysis'):
        st.subheader('Customer Segment Analysis')
        segment = st.selectbox('Select a customer segment', 
                               options=['Gender', 'Customer type', 'Branch'])
        metric = st.selectbox('Select a metric', 
                              options=['Total', 'Quantity', 'Rating'])
        
        fig = px.box(df, x=segment, y=metric, color=segment)
        fig.update_layout(title=f'{metric} Distribution by {segment}')
        st.plotly_chart(fig)
        st.write(f"This box plot shows the distribution of {metric} across different {segment} categories.")

    # New feature: Product Performance Dashboard
    with st.expander('Product Performance Dashboard'):
        st.subheader('Product Performance Dashboard')
        product_line = st.selectbox('Select a product line', 
                                    options=df['Product line'].unique())
        
        filtered_df = df[df['Product line'] == product_line]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(filtered_df, values='Quantity', names='Branch', 
                          title=f'Quantity Sold by Branch for {product_line}')
            st.plotly_chart(fig1)
        
        with col2:
            fig2 = px.bar(filtered_df, x='Branch', y='Total', 
                          title=f'Total Sales by Branch for {product_line}')
            st.plotly_chart(fig2)
        
        fig3 = px.scatter(filtered_df, x='Unit price', y='Quantity', 
                          color='Branch', size='Rating', hover_data=['Total'],
                          title=f'Price vs Quantity for {product_line}')
        st.plotly_chart(fig3)