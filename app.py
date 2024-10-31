import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

import pandas as pd

import seaborn as sns

import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="SuperStore!!!", page_icon=":bar_chart:",layout="wide")

st.title(":bar_chart: :blue[SuperStore Interactive Sales Dashboard]")   

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    url = "https://raw.githubusercontent.com/mohamadkamel010/interactive_dashboard/refs/heads/main/data_sales.csv"
    df = pd.read_csv(url, encoding = "ISO-8859-1")


df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year


start_date = df["Order Date"].min()
end_date = df["Order Date"].max()

col1,col2 = st.columns((2))

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date',start_date))

with col2:
    date2 = pd.to_datetime(st.date_input('End Date',end_date))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# Adding Filters
st.sidebar.header('Choose Your Filter: ')

# Create filter for State
state = st.sidebar.multiselect("Pick the State", df['State'].unique())
if not state:
    df2 = df.copy()
else:
    df2 = df[df['State'].isin(state)]

# Create filter for City
city = st.sidebar.multiselect("Pick the City", df2['City'].unique())
if not city:
    df3 = df2.copy()
else:
    df3 = df2[df2['City'].isin(city)]

# Create filter for Year
year = st.sidebar.multiselect("Pick the Year", df3['Year'].unique())
if not year:
    df4 = df3.copy()
else:
    df4 = df3[df3['Year'].isin(year)]    

# Create filter for Month
month = st.sidebar.multiselect("Pick the Month", df4['Month'].unique())
if not month:
    df5 = df4.copy()
else:
    df5 = df4[df4['Month'].isin(month)]     

# Create filter for Day
day = st.sidebar.multiselect("Pick the Day", df5['Day'].unique())
if not day:
    df6 = df5.copy()
else:
    df6 = df5[df5['Day'].isin(day)]  

# Create filtered DateSet based on Specific Filters
def df_filtered(
    df: pd.DataFrame,  
    f_state: list = [], 
    f_city: list = [],  
    f_year: list = [], 
    f_month: list = [],  
    f_day: list = [],
) -> pd.DataFrame:
    if len(f_state) > 0:
        df = df6.loc[(df6['State'].isin(state))].reset_index(drop=True)
    if len(f_city) > 0:
        df = df6.loc[(df6['City'].isin(city))].reset_index(drop=True)
    if len(f_year) > 0:
        df = df6.loc[(df6['Year'].isin(year))].reset_index(drop=True)
    if len(f_month) > 0:
        df = df6.loc[(df6['Month'].isin(month))].reset_index(drop=True)        
    if len(f_day) > 0:
        df = df6.loc[(df6['Day'].isin(day))].reset_index(drop=True)        
    return df

filtered_df = df_filtered(df,f_state=state,f_city=city,f_year=year,f_month=month,f_day=day)

#Create grouped datasets
month_df = filtered_df.groupby('Month')['Sales'].sum().sort_values(ascending=False).reset_index()
day_df = filtered_df.groupby('Day')['Sales'].sum().sort_values(ascending=False).reset_index()
state_df = filtered_df.groupby('State')['Sales'].sum().sort_values(ascending=False).reset_index()
city_df = filtered_df.groupby('City')['Sales'].sum().sort_values(ascending=False).reset_index()

#State Wise Sales
with col1:
    st.subheader("State Wise Sales")
    fig = px.bar(state_df, x = "State", y = "Sales", text = ['${:,.2f}'.format(x) for x in state_df["Sales"]],
                 template = "seaborn",color='State', labels={'Sales':'Total Volume of Sales in (M$)'})
    st.plotly_chart(fig,use_container_width=True, height = 200)

#City Wise Sales
with col2:
    st.subheader("City Wise Sales")
    fig = px.bar(city_df, x = "City", y = "Sales", text = ['${:,.2f}'.format(x) for x in city_df["Sales"]],
                 template = "seaborn",color='City',labels={'Sales':'Total Volume of Sales in (M$)'})
    st.plotly_chart(fig,use_container_width=True, height = 200) 

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("State_Sales_ViewData"):
        st.write(state_df.style.background_gradient(cmap="Blues"))
        csv = state_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "State_Sales.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("City_Sales_ViewData"):
        st.write(city_df.style.background_gradient(cmap="Oranges"))
        csv = city_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "City_Sales.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')       

st.divider()

col3,col4 = st.columns((2))

#Month Wise Sales
with col3:
    st.subheader("Month Wise Sales")
    fig = px.bar(month_df, x = "Month", y = "Sales", text = ['${:,.2f}'.format(x) for x in month_df["Sales"]],
                 template = "seaborn",color='Month',labels={'Sales':'Total Volume of Sales in (M$)'})
    st.plotly_chart(fig,use_container_width=True, height = 200)

#Day Wise Sales
with col4:
    st.subheader("Day Wise Sales")
    fig = px.bar(day_df, x = "Day", y = "Sales", text = ['${:,.2f}'.format(x) for x in day_df["Sales"]],
                 template = "seaborn",color='Day',labels={'Sales':'Total Volume of Sales in (M$)'})
    st.plotly_chart(fig,use_container_width=True, height = 200)  

cl5, cl6 = st.columns((2))
with cl5:
    with st.expander("Month_Sales_ViewData"):
        st.write(month_df.style.background_gradient(cmap="Blues"))
        csv = month_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Month_Sales.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl6:
    with st.expander("Day_Sales_ViewData"):
        st.write(day_df.style.background_gradient(cmap="Oranges"))
        csv = day_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Day_Sales.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')  

st.divider()

# Total Volume of Sales per Hour
hour_sales_df = filtered_df.groupby('Hour')['Sales'].sum().reset_index()
st.subheader('Time Series Analysis: Total Volume of Sales per Hour')
fig2 = px.line(hour_sales_df, x = "Hour", y="Sales",height=500, width = 1000,template="gridon",
               labels={'Sales':'Total Volume of Sales (M$)'})

fig2.update_xaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10,tick0=0, dtick=1)
fig2.update_yaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10, col=1)

st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(hour_sales_df.T.style.background_gradient(cmap="Blues"))
    csv = hour_sales_df.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "Sales_per_Hour.csv", mime ='text/csv')

st.divider()

# Total Number of Orders per Hour
st.subheader('Time Series Analysis: Number of Orders Per Hour')

hour_df = pd.DataFrame(filtered_df.groupby('Hour')['Order ID'].count().reset_index())
fig2 = px.line(hour_df, x = "Hour", y="Order ID",height=500, width = 1000,template="gridon",
               labels={"Order ID":'Number of Orders'})
fig2.update_xaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10,tick0=0, dtick=1)
fig2.update_yaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10, col=1)

st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(hour_df.T.style.background_gradient(cmap="Blues"))
    csv = hour_df.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "Orders_per_Hour.csv", mime ='text/csv')

st.divider()

#The relation Between Quantity Ordered and its Prices
st.subheader("The relation Between Quantity Ordered and its Prices")

product_df = filtered_df.groupby('Product')['Quantity Ordered'].sum().reset_index()
prices = filtered_df.groupby('Product').max()['Price Each'].reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Bar(x = product_df['Product'], y = product_df['Quantity Ordered'], name = 'Quantity Ordered'))
fig3.add_trace(go.Scatter(x=prices['Product'], y = prices['Price Each'], mode = "lines",
                          name ='Price Each', yaxis="y2"))
fig3.update_layout(
    xaxis = dict(title='Product'),
    yaxis = dict(title='Number of Quantity Ordered', showgrid = False),
    yaxis2 = dict(title='Price Each in($)', overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)

st.plotly_chart(fig3,use_container_width=True)

col7, col8 = st.columns((2))
with col7:
    with st.expander("View the Quantity Ordered"):
        st.write(product_df.style.background_gradient(cmap="Blues"))
        csv = product_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Quantity_Orderd_by_Product.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with col8:
    with st.expander("View the Price of Products"):
        st.write(prices.style.background_gradient(cmap="Greens"))
        csv = prices.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Products_Prices.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file') 

st.divider()

# Top Bundles of Products Sold Togther
st.subheader("Top Products Sold in Bundles")

col9, col10 = st.columns((2))

with col9:
     num = st.selectbox('Enter the number of products sold in one bundle:',[1,2,3,4])
with col10:     
     top = st.selectbox('Enter the top number of bundles for sold products:',[1,2,3,4,5,6,7,8,9,10])

grouped_data = filtered_df[filtered_df.duplicated('Order ID', keep=False)]
grouped_data['Grouped'] = grouped_data.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
grouped_data = grouped_data[['Order ID', 'Grouped']].drop_duplicates()
from itertools import combinations
from collections import Counter
count = Counter()
for row in grouped_data['Grouped']:
   row_list = row.split(',')
   count.update(Counter(combinations(row_list, num)))
product_group = []   
for key,value in count.most_common(top): 
    product_group.append({'Group_Products':list(key),'Number of Bundles':value})
    
product_group = pd.DataFrame(product_group,columns=product_group[0].keys())

st.subheader(f"View the top ({top}) of {num} Products Sold in Bundles:")
st.write(product_group.style.background_gradient(cmap="Oranges"))
csv =  product_group.to_csv(index = False).encode('utf-8')
st.download_button("Download Data", data = csv, file_name = f"Top ({top}) Bundles of {num} Products_Sold_togther.csv", mime = "text/csv",
                   help = 'Click here to download the data as a CSV file') 

st.divider()

#Adding Information about Auther

col11,col12 = st.columns((2))

html_footer = """
<footer>
  <p>Content By: Mohammed Kamel A.Haliem</p>
  <p><a href="mailto:mohamad.kamel013@gmail.com">mohamad.kamel013@gmail.com</a></p>
</footer>"""

with col11:
    st.markdown(html_footer, unsafe_allow_html=True)
