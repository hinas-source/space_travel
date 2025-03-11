import streamlit as st
import time
import datetime
import random
import os
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Space destinations & pricing
DESTINATIONS = {
    "International Space Station": {"economy": 500000, "luxury": 1200000, "VIP": 2500000},
    "Lunar Hotel": {"economy": 1500000, "luxury": 3000000, "VIP": 5000000},
    "Mars Colony": {"economy": 5000000, "luxury": 10000000, "VIP": 20000000},
}

# Get current user (Mocked for demo purposes)
def get_current_user():
    return "user@example.com"

# Space Accommodations
ACCOMMODATIONS = {
    "International Space Station": ["Orbital Suites", "Cosmo Cabins"],
    "Lunar Hotel": ["Moonlight Resort", "Lunar Lux Villas"],
    "Mars Colony": ["Red Planet Lodges", "Martian Domes"]
}

# Launch Countdown
def launch_countdown(departure_date):
    now = datetime.datetime.now()
    launch_time = datetime.datetime.strptime(departure_date, "%Y-%m-%d")
    return (launch_time - now).days

# Streamlit UI
st.title("🚀 Dubai to the Stars – Book Your Space Travel")

st.sidebar.header("User Dashboard")
current_user = get_current_user()
st.sidebar.write(f"**Logged in as:** {current_user}")

# Booking Form
st.subheader("🌌 Book Your Space Journey")
destination = st.selectbox("Choose Destination", list(DESTINATIONS.keys()))
departure_date = st.date_input("Select Departure Date", min_value=datetime.date.today())
seat_class = st.radio("Select Class", ["economy", "luxury", "VIP"])

price = DESTINATIONS[destination][seat_class]
st.write(f"💰 **Price:** ${price:,}")

if st.button("Book Now"):
    booking_data = {"user": current_user, "destination": destination, "date": str(departure_date), "class": seat_class, "price": price}
    supabase.table("bookings").insert(booking_data).execute()
    st.success("🎟️ Booking Confirmed! Check Dashboard for details.")

# Accommodation Suggestions
st.subheader("🏨 Recommended Accommodations")
st.write(random.choice(ACCOMMODATIONS[destination]))

# Dashboard with Countdown
st.sidebar.subheader("🚀 Upcoming Launch")
countdown_days = launch_countdown(str(departure_date))
st.sidebar.write(f"**{countdown_days} days until launch!**")
