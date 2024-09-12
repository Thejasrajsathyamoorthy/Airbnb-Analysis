import json
import pandas as pd
import psycopg2
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px



# SQL Connection

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "Airbnb_Analysis",
                        password = "Thejas@4218")

cursor = mydb.cursor()

# Hotel Details

cursor.execute("SELECT * FROM Hotel_Details")
mydb.commit()
hotel_data_table = cursor.fetchall()

Hotel_Data = pd.DataFrame(hotel_data_table, columns=("Hotel_Id", "Hotel_Name", "Hotel_url", "Description", "Property_type", "Room_type", "Bed_type",
                                                        "Accomodates", "Min_nights", "Price", "Availability_365", "Amenities", "Neighbourhood",
                                                            "Neighbourhood_Group", "City", "Country", "latitude", "longitude", "Host_Id", "Host_Name",
                                                                "Host_url", "Total_listing_by_Host", "Num_of_review", "Review_rating"))



# Review Details

cursor.execute("SELECT * FROM Review_Details")
mydb.commit()
review_data_table = cursor.fetchall()

Review_Data = pd.DataFrame(review_data_table, columns=( "Hotel_Id", "Hotel_Name", "Reviewer_Id", "Reviewer_Name", "Comments"))



# Hotel Data Exploration

def Hotel_Details(data):
    airbnb_hotel_data = []

    for item in data:
        Hotel_data = {
                "Hotel_Id": item.get("_id"),
                "Hotel_Name": item.get("name"),
                "Hotel_url": item.get("listing_url"),
                "Description": item.get("description"),
                "Property_type" : item.get("property_type"),
                "Room_type" : item.get("room_type"),
                "Bed_type": item.get("bed_type"),
                "Accomodates": item.get("accommodates"),
                "Min_nights": item.get("minimum_nights"),
                "Price": item.get("price"),
                "Availability_365": item.get("availability", {}).get("availability_365"),
                "Amenities": item.get("amenities"),
                "Neighborhood" : item.get("address",{}).get("government_area"),
                "Neighborhood_group" : item.get("address",{}).get("suburb"),
                "City" : item.get("address",{}).get("market"),
                "Country" : item.get("address",{}).get("country"),
                "latitude": item.get("address", {}).get("location", {}).get("coordinates")[1],
                "longitude": item.get("address", {}).get("location", {}).get("coordinates")[0],
                "Host_Id": item.get("host", {}).get("host_id"),
                "Host_Name": item.get("host", {}).get("host_name"),
                "Host_url": item.get("host",{}).get("host_url"),
                "Total_listing_by_Host" : item.get("host",{}).get("host_total_listings_count"),
                "Num_of_review" : item.get("number_of_reviews"),
                "Review_rating": item.get("review_scores", {}).get("review_scores_rating")}
                
            
        airbnb_hotel_data.append(Hotel_data)
    Airbnb_Hotel_df = pd.DataFrame(airbnb_hotel_data)

    return Airbnb_Hotel_df



# Filter by Country

def filter_by_country(country):
    Select_country = Hotel_Data[Hotel_Data["Country"] == country]
    Select_country.reset_index(drop= True, inplace= True)



    Select_country = pd.DataFrame(Select_country)

    return Select_country



# Filter by City

def filter_by_city(city):
    Select_City = Country[Country["City"] == city]
    Select_City.reset_index(drop= True, inplace= True)

    Select_City = pd.DataFrame(Select_City)

    return Select_City



# Filter by Neighbouhood group

def filter_by_neighbour_group(neighour_group):
    Select_Neighbour_group = City[City["Neighbourhood_Group"] == neighour_group]
    Select_Neighbour_group.reset_index(drop= True, inplace= True)

    Select_Neighbour_group = pd.DataFrame(Select_Neighbour_group)

    return Select_Neighbour_group



# Filter Comment by Hotel Id 

def Filter_cmt_by_Hotel_Id(Hotel_Id):
    Select_Hotel = Review_Data[Review_Data["Hotel_Id"] == Hotel_Id]
    Select_Hotel.reset_index(drop= True, inplace= True)

    Select_Hotel = pd.DataFrame(Select_Hotel)

    return Select_Hotel


# Filter by Price

def Filter_Hotel_by_Price(Min_price,Max_price):
    Select_Price = Neighbour_group[(Neighbour_group["Price"] >= Min_price) & (Neighbour_group["Price"] <= Max_price)]
    Select_Price.reset_index(drop= True, inplace= True)

    Select_Price = pd.DataFrame(Select_Price)

    return Select_Price


def Filter_Hotels(Filtered_Hotels):
    Selected_Hotels = fltrd_by_Price[fltrd_by_Price["Hotel_Id"] == Filtered_Hotels]
    Selected_Hotels.reset_index(drop= True, inplace= True)

    Selected_Hotels = pd.DataFrame(Selected_Hotels)

    return Selected_Hotels

    
## Streamlit part

st.set_page_config(page_title = "Airbnb Analysis", page_icon = ":bar_chart:",layout= "wide")
st.title(":bar_chart:  Airbnb Analysis")

st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html= True)

with st.sidebar:
    select = option_menu("Main menu", ["Home","Data Exploration", "Analysis"])


# Home Page

if select == "Home":
    col1,col2 = st.columns([10,5])
    with col1:
        st.markdown("### :red[**_Airbnb, Inc._**] is an American company operating an online marketplace for short and long-term homestays and experiences in various countries and regions. Airbnb full form is :orange[_**'Air Bed and Breakfast**'_], The company acts as a broker and charges a commission from each booking. Airbnb was founded in August 2008. It is the most well-known company for short-term housing rentals.")
    
    with col2:
        st.image("C:/Users/Theju/Desktop/Guvi Capstone Projects/Airbnb Analysis/Airbnb_Logo.png", width=450)

    col1, col2 = st.columns([14,8])
    with col1:
        st.write("\n")
        st.markdown("#### :blue[_Problem Statement_ :] This project aims to analyze Airbnb data perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
        st.markdown("#### :blue[_Skills take away_ :] Python scripting, Data Pre-processing, Visualization, EDA, Streamlit, PowerBI or Tableau.")
        st.markdown("#### :blue[_Domain_:] Travel Industry, Property Management and Tourism")

    # with col3:
    st.write("\n")
    st.markdown("### :red[**_Outcome_ :**] In this Project, after performing Pre-processing and EDA in sample datas it comes out as clean data. With these datas usefull insights are collected and visualizaion process done.")



# Data Exploration Part

elif select == "Data Exploration":
    col1, col2 = st.columns(2)

    with col1:
        File_upload = st.file_uploader("Choose the file")

    if File_upload:
        col1,col2 = st.columns(2)
        with col1:
            st.success("File uploaded")
        data = json.load(File_upload)
        
        st.subheader("Hotel Data")
        st.write(Hotel_Details(data))
        
        st.subheader("Review Data")
        col1, col2 = st.columns(2)
        with col1:
            Hotel_Id = st.selectbox("Select Hotel_Id",Review_Data["Hotel_Id"].unique())
        st.write(Filter_cmt_by_Hotel_Id(Hotel_Id))

    else:
        st.info("Choose file to upload")

# Analysis Part

elif select == "Analysis":
        
        col1, col2, col3 = st.columns([8, 1, 8])

        with col1:
            country = st.selectbox("Filter by Country,", Hotel_Data["Country"].unique())
            Country = filter_by_country(country)

            city = st.selectbox("Filter by City,", Country["City"].unique())
            City = filter_by_city(city)

        with col3:
            neighour_group = st.selectbox("Filter by Neighbour group,", City["Neighbourhood_Group"].unique())
            Neighbour_group = filter_by_neighbour_group(neighour_group)

            Min_price, Max_price = st.slider("Price range,", value=[ Neighbour_group["Price"].min(), Neighbour_group["Price"].max()])
            fltrd_by_Price = Filter_Hotel_by_Price(Min_price,Max_price)
            st.write("\n")
            st.write("\n")
            st.write(fltrd_by_Price)


        with col1:
            st.write("\n")
            st.write("\n")
            st.map(fltrd_by_Price[["latitude","longitude"]],use_container_width= True)


        col1, col2, col3 = st.columns([8,1,8])
        with col1:
            Property_grp = fltrd_by_Price.groupby("Property_type")["Price"].mean().reset_index(name = "Avg_Price")

            Property_bar = px.bar(Property_grp, x= "Property_type", y= "Avg_Price" , title= "Property type and its Avg Price", color= "Property_type",
                                    hover_name= "Property_type",)
            st.plotly_chart(Property_bar)

        with col3:
            Room_grp = fltrd_by_Price.groupby("Room_type")["Accomodates"].median().reset_index(name = "Accomodates")

            Room_bar = px.bar(Room_grp, x= "Room_type", y= "Accomodates" , title= "Room type and it Accomodates", color= "Room_type",
                                    hover_name= "Room_type",)
            st.plotly_chart(Room_bar)

