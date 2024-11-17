import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import os

# Set page title and configuration
st.set_page_config(page_title="Deal Hunter - DealsHeaven", page_icon="🛍", layout="centered")
st.title("🛍 Deal Hunter")
st.subheader("Your Ultimate Deal Finder!")
st.write("Find the best deals from your favorite stores in seconds!")

# Add instructions for store selection
st.write("### Select a Store to Explore Deals:")
store_name = st.selectbox(
    "Choose a store from the list below:",
    options=[
        "Amazon", "Airasia", "Aircel", "AmericanSwan", "askmebazar", "Abhibus", "AkbarTravels", "abof", "Airtel",
        "Babyoye", "Bigrock", "Burgerking", "Bigbasket", "bookmyshow", "Bluehost", "cromaretail", "Cleartrip",
        "crownit", "Cinepolis Cinema", "Clovia", "Dominos", "Ebay", "Edukart", "Expedia", "EaseMyTrip", "Flipkart",
        "Firstcry", "Fasttrack", "FashionAndYou", "Fabfurnish", "Fabindia", "Fashionara", "fernsnpetals", "Foodpanda",
        "Freecharge", "Freecultr", "Fasoos", "FitnLook", "Goibibo", "Groupon India", "Grofers", "Greendust", "GoAir",
        "Helpchat", "HomeShop18", "HealthKart", "Hostgator", "Indiatimes", "Infibeam", "ixigo", "IndiGo", "Jabong",
        "Jugnoo", "JustRechargeIt", "Koovs", "KFC", "LensKart", "LittleApp", "MakeMyTrip", "McDonalds", "Mobikwik",
        "Musafir", "Myntra", "Nearbuy", "Netmeds", "NautiNati", "Nykaa", "Others", "Oyorooms", "Ola", "Paytm",
        "PayUMoney", "Pepperfry", "Printvenue", "PayZapp", "Pizzahut", "Photuprint", "pharmeasy", "Redbus", "Rediff",
        "Rewardme", "Reliance Big TV", "Reliance trends", "Snapdeal", "ShopClues", "ShoppersStop", "Sweetsinbox",
        "Styletag", "ShopCJ", "Taxi for Sure", "Travelguru", "Trendin", "ticketnew", "TataCLiQ", "Tata Sky",
        "thyrocare", "udio", "UseMyVoucher", "Uber", "voonik", "Vistaprint", "VLCC", "VideoconD2H", "Vodafone",
        "Woo Hoo", "Woodland", "Yatra", "Yepme", "Zivame", "Zovi", "Zomato", "zoomin", "Zotezo"
    ]
)

# Instructions for page range
st.write("### Define Page Range to Search Deals:")
start_page = st.number_input("Enter Start Page (Minimum: 1)", min_value=1, step=1, format="%d")
end_page = st.number_input("Enter End Page (Must be greater than or equal to Start Page)", min_value=1, step=1, format="%d")

# Search Deals Button
if st.button("Search Deals"):
    if end_page < start_page:
        st.error("End Page should be greater than or equal to Start Page.")
    else:
        st.info("Fetching data... Please wait.")
        all_deals = []

        # Loop through the selected page range
        for page in range(start_page, end_page + 1):
            url = f"https://dealsheaven.in/store/{store_name.lower()}?page={page}"
            response = requests.get(url)

            # Check if the page is accessible
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find deal cards
                deal_cards = soup.find_all('div', class_='deatls-inner')

                for deal_card in deal_cards:
                    title = deal_card.find('h3').text.strip() if deal_card.find('h3') else "No title"
                    price = deal_card.find('p', class_='price').text.strip() if deal_card.find('p', class_='price') else "No price"
                    special_price = deal_card.find('p', class_='spacail-price').text.strip() if deal_card.find('p', class_='spacail-price') else "No special price"

                    # Calculate discount percentage if both prices are available
                    try:
                        original_price = float(price.replace('₹', '').replace(',', ''))
                        discounted_price = float(special_price.replace('₹', '').replace(',', ''))
                        discount_percentage = round(((original_price - discounted_price) / original_price) * 100, 2)
                    except:
                        discount_percentage = "N/A"

                    all_deals.append({
                        "Title": title,
                        "Original Price": price,
                        "Special Price": special_price,
                        "Discount Percentage": f"{discount_percentage}%" if isinstance(discount_percentage, float) else "N/A"
                    })
            else:
                st.warning(f"Page {page} could not be accessed. Status code: {response.status_code}")

        # Save to CSV
        if all_deals:
            deals_df = pd.DataFrame(all_deals)
            csv_file = f"{store_name}deals_page{start_page}to{end_page}.csv"
            deals_df.to_csv(csv_file, index=False)
            st.success(f"Deals successfully saved to {csv_file}")

            # Display the deals in a table
            st.subheader(f"Deals for {store_name} from page {start_page} to {end_page}:")
            st.dataframe(deals_df)
        else:
            st.warning("No deals found for the selected store and page range.")
