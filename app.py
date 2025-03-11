import streamlit as st
import datetime
from supabase import create_client, Client
import random

import re

# Function to handle user sign-up with basic email validation
def signup_user(email: str, password: str):

    email = email.strip()
    
    # Basic regex for email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if not re.match(email_regex, email):
        st.error("Invalid email format. Please enter a valid email address.")
        return

    # Debug information (you can remove this later)
    st.info(f"Attempting to sign up with email: '{email}' (length: {len(email)})")

    try:
        # Use named parameters format instead of dictionary
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if hasattr(response, 'error') and response.error:
            st.error(f"Sign up failed: {response.error.message}")
        else:
            st.success("Sign-up successful! Please check your email to confirm.")
    except Exception as e:
        st.error(f"Sign up failed: {str(e)}")
        
        # Additional debugging for specific error types
        error_text = str(e)
        if "is invalid" in error_text:
            st.warning("Try using a different email address - Supabase may have specific requirements.")
            st.info("For testing, try creating a real email or using services like 'temp-mail.org'")


# Initialize Supabase client
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to handle user login
def login_user(email: str, password: str):
    response = supabase.auth.sign_in(email=email, password=password)
    if response.error:
        st.error(f"Login failed: {response.error.message}")
    else:
        st.session_state.user = response.user
        st.success("Logged in successfully")


# Function to log out user
def logout_user():
    supabase.auth.sign_out()
    del st.session_state.user
    st.success("Logged out successfully")

# Check if user is logged in
def is_logged_in():
    return "user" in st.session_state

# Space destinations & pricing
DESTINATIONS = {
    "International Space Station": {"economy": 500000, "luxury": 1200000, "VIP": 2500000},
    "Lunar Hotel": {"economy": 1500000, "luxury": 3000000, "VIP": 5000000},
    "Mars Colony": {"economy": 5000000, "luxury": 10000000, "VIP": 20000000},
}

# Booking Form
def booking_form():
    st.subheader("🌌 Book Your Space Journey")
    destination = st.selectbox("Choose Destination", list(DESTINATIONS.keys()))
    departure_date = st.date_input("Select Departure Date", min_value=datetime.date.today())
    seat_class = st.radio("Select Class", ["economy", "luxury", "VIP"])

    # Display price based on seat class
    price = DESTINATIONS[destination][seat_class]
    st.write(f"💰 **Price:** ${price:,}")

    if st.button("Book Now"):
        # Capture booking details
        current_user = st.session_state.user.email
        booking_data = {
            "user_email": current_user,
            "destination": destination,
            "date": str(departure_date),
            "class": seat_class,
            "price": price,
        }
        
        # Insert data into Supabase
        response = supabase.table("bookings").insert(booking_data).execute()
        if response.status_code == 201:
            st.success("🎟️ Booking Confirmed! Check Dashboard for details.")
        else:
            st.error("⚠️ There was an error with your booking.")

# User Dashboard
def user_dashboard():
    st.header(f"Welcome, {st.session_state.user.email}")
    st.button("Logout", on_click=logout_user)

    # Fetch user bookings from Supabase
    user_bookings = supabase.table("bookings").select("*").eq("user_email", st.session_state.user.email).execute()

    if user_bookings.data:
        for booking in user_bookings.data:
            st.write(f"**Destination:** {booking['destination']}")
            st.write(f"**Class:** {booking['class']}")
            st.write(f"**Price:** ${booking['price']:,}")
            st.write(f"**Departure Date:** {booking['date']}")
    else:
        st.write("You have no active bookings.")

# Main page layout
st.title("🚀 Dubai to the Stars – Book Your Space Travel")

# Login/Sign-Up UI
if not is_logged_in():
    menu = st.radio("Choose an action", ["Login", "Sign Up"])

    if menu == "Login":
        email = st.text_input("Email")

        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if email and password:
                login_user(email, password)
            else:
                st.error("Please enter both email and password.")

    elif menu == "Sign Up":
        email = st.text_input("Email")
        
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            if email and password:
                signup_user(email, password)
            else:
                st.error("Please enter both email and password.")
else:
    # Once logged in, show either the booking form or the user dashboard
    menu = st.sidebar.selectbox("Select Menu", ["Trip Scheduling & Booking", "User Dashboard"])
    
    if menu == "Trip Scheduling & Booking":
        booking_form()

    elif menu == "User Dashboard":
        user_dashboard()
