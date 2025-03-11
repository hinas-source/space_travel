import streamlit as st
import time
import datetime
import random
import os
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL =  "https://sbdedhvzitxgvxsnkxqc.supabase.co" #os.getenv("SUPABASE_URL")
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNiZGVkaHZ6aXR4Z3Z4c25reHFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE2NTg0NTEsImV4cCI6MjA1NzIzNDQ1MX0.NiASD4LrhnZEcywurrNxhc4zD5GoKLbLNEUWiimIgpY" #os.getenv("SUPABASE_KEY")
#st.write("SUPABASE_URL:", os.getenv("SUPABASE_URL"))  # Debugging
#st.write("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))  # Debugging

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
    launch_time = datetime.datetime.strptime(str(departure_date), "%Y-%m-%d").date()
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
    booking_data = {
        "user": current_user,
        "destination": destination,
        "date": str(departure_date),
        "class": seat_class,
        "price": price
    }
    #supabase.table("bookings").insert(booking_data).execute()
    try:
        with st.spinner("Processing your booking..."):
            response = supabase.table("bookings").insert(booking_data).execute()
            st.success("🎟️ Booking Confirmed! Check Dashboard for details.")
            st.write(f"**Destination:** {destination}")
            st.write(f"**Departure Date:** {departure_date}")
            st.write(f"**Class:** {seat_class.capitalize()}")
            st.write(f"**Total Price:** ${price:,}")
    except Exception as e:
        st.error(f"Booking failed: {e}")

    st.success("🎟️ Booking Confirmed! Check Dashboard for details.")

# Accommodation Suggestions
st.subheader("🏨 Recommended Accommodations")
for accommodation in ACCOMMODATIONS[destination]:
    st.write(f"- {accommodation}")

# Dashboard with Countdown
st.sidebar.subheader("🚀 Upcoming Launch")
countdown_days = launch_countdown(departure_date)
st.sidebar.write(f"**{countdown_days} days until launch!**")
