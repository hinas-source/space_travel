import streamlit as st
import datetime
from supabase import create_client, Client
import random
import os

# Initialize Supabase client
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials are missing. Please set environment variables.")
    st.stop()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Space destinations & pricing
DESTINATIONS = {
    "International Space Station": {"economy": 500000, "luxury": 1200000, "VIP": 2500000},
    "Lunar Hotel": {"economy": 1500000, "luxury": 3000000, "VIP": 5000000},
    "Mars Colony": {"economy": 5000000, "luxury": 10000000, "VIP": 20000000},
}

# Accommodation suggestions based on destination
ACCOMMODATIONS = {
    "International Space Station": ["Orbital Suites", "Cosmo Cabins"],
    "Lunar Hotel": ["Moonlight Resort", "Lunar Lux Villas"],
    "Mars Colony": ["Red Planet Lodges", "Martian Domes"]
}

# Launch Countdown
def launch_countdown(departure_date):
    now = datetime.datetime.now().date()
    launch_time = datetime.datetime.strptime(str(departure_date), "%Y-%m-%d").date()
    return (launch_time - now).days


# Main page layout
st.title("🚀 Dubai to the Stars – Book Your Space Travel")

menu = ["Trip Scheduling & Booking", "Pricing & Packages", "Accommodation Recommendations", "User Dashboard"]
choice = st.sidebar.selectbox("Select Menu", menu)

if choice == "Trip Scheduling & Booking":
    # Display the booking form
    st.subheader("🌌 Book Your Space Journey")
    destination = st.selectbox("Choose Destination", list(DESTINATIONS.keys()))
    departure_date = st.date_input("Select Departure Date", min_value=datetime.date.today())
    seat_class = st.radio("Select Class", ["economy", "luxury", "VIP"])

    price = DESTINATIONS[destination][seat_class]
    st.write(f"💰 **Price:** ${price:,}")

    if st.button("Book Now"):
        # Insert booking details into Supabase
        current_user = "user@example.com"  # Mocked user data for demo
        booking_data = {
            "user_email": current_user,
            "destination": destination,
            "date": str(departure_date),
            "class": seat_class,
            "price": price,
        }

        response = supabase.table("bookings").insert(booking_data).execute()
        if response.status_code == 201:
            st.success("🎟️ Booking Confirmed! Check Dashboard for details.")
        else:
            st.error("⚠️ There was an error with your booking.")

elif choice == "Pricing & Packages":
    # Display travel packages and prices
    st.subheader("💼 Pricing & Packages")
    for destination, prices in DESTINATIONS.items():
        st.write(f"### {destination}")
        for seat_class, price in prices.items():
            st.write(f"**{seat_class.capitalize()} Class:** ${price:,}")

elif choice == "Accommodation Recommendations":
    # Display accommodation recommendations
    st.subheader("🏨 Recommended Accommodations")
    destination = st.selectbox("Choose your Destination for Accommodation Suggestions", list(ACCOMMODATIONS.keys()))
    recommended_accommodation = random.choice(ACCOMMODATIONS[destination])
    st.write(f"**Recommended Accommodation:** {recommended_accommodation}")

elif choice == "User Dashboard":
    # Display user dashboard with bookings and countdown
    st.header("User Dashboard")
    current_user = "user@example.com"  # Mocked for demo purposes
    st.write(f"**Logged in as:** {current_user}")

    # Fetch and display bookings
    user_bookings = supabase.table("bookings").select("*").eq("user_email", current_user).execute()

    if user_bookings.data:
        for booking in user_bookings.data:
            st.write(f"**Destination:** {booking['destination']}")
            st.write(f"**Class:** {booking['class']}")
            st.write(f"**Price:** ${booking['price']:,}")
            st.write(f"**Departure Date:** {booking['date']}")
            # Countdown timer to launch
            launch_date = datetime.datetime.strptime(booking['date'], "%Y-%m-%d")
            days_until_launch = (launch_date - datetime.datetime.now()).days
            st.write(f"**Launch Countdown:** {days_until_launch} days left")

    else:
        st.write("You have no active bookings.")
        
    # AI Travel Tips Section
    st.subheader("AI Travel Tips")
    st.write("🚀 Tip: To prepare for zero-gravity, practice floating in water! 💧")

