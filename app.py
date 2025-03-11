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
    "International Space Station": {"Economy": 500000, "Luxury": 1200000, "VIP": 2500000},
    "Lunar Hotel": {"Economy": 1500000, "Luxury": 3000000, "VIP": 5000000},
    "Mars Colony": {"Economy": 5000000, "Luxury": 10000000, "VIP": 20000000},
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
    seat_class = st.radio("Select Class", ["Economy", "Luxury", "VIP"])

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

        try:
            response = supabase.table("bookings").insert(booking_data).execute()
            if hasattr(response, "data") and response.data:
                st.success("🎟️ Booking Confirmed! Check Dashboard for details.")
            else:
                st.error("⚠️ There was an error with your booking.")
        except Exception as e:
            st.error(f"⚠️ Booking error: {str(e)}")

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
    st.header("👤 User Dashboard")
    current_user = "user@example.com"  # Mocked for demo purposes
    st.write(f"**Logged in as:** {current_user}")

    # Initialize session state for booking cancellation if it doesn't exist
    if 'show_cancel_confirmation' not in st.session_state:
        st.session_state.show_cancel_confirmation = False
    if 'booking_to_cancel' not in st.session_state:
        st.session_state.booking_to_cancel = None
        
    # Fetch and display bookings
    user_bookings = supabase.table("bookings").select("*").eq("user_email", current_user).execute()

    if user_bookings.data:
        st.subheader("🎟️ Your Bookings")
        
        # Create columns for the bookings grid
        col1, col2 = st.columns(2)
        
        # Display bookings in a grid of cards
        for i, booking in enumerate(user_bookings.data):
            # Alternate between columns
            current_col = col1 if i % 2 == 0 else col2
            
            with current_col:
                with st.container():
                    st.markdown("---")
                    # Calculate countdown
                    launch_date = datetime.datetime.strptime(booking['date'], "%Y-%m-%d")
                    days_until_launch = (launch_date - datetime.datetime.now()).days
                    
                    # Show countdown with appropriate styling
                    if days_until_launch < 0:
                        countdown_color = "red"
                        countdown_text = f"**LAUNCHED** ({abs(days_until_launch)} days ago)"
                    elif days_until_launch == 0:
                        countdown_color = "orange"
                        countdown_text = "**LAUNCHING TODAY!**"
                    elif days_until_launch <= 7:
                        countdown_color = "orange"
                        countdown_text = f"**LAUNCHING SOON:** {days_until_launch} days left"
                    else:
                        countdown_color = "green"
                        countdown_text = f"**Launch Countdown:** {days_until_launch} days left"
                    
                    # Create a card-like appearance
                    st.markdown(f"### 🚀 Trip to {booking['destination']}")
                    
                    # Create two columns within the card for better layout
                    detail_col1, detail_col2 = st.columns(2)
                    
                    with detail_col1:
                        st.write(f"**Class:** {booking['class'].capitalize()}")
                        st.write(f"**Price:** ${booking['price']:,}")
                    
                    with detail_col2:
                        st.write(f"**Departure:** {booking['date']}")
                        st.markdown(f":<span style='color:{countdown_color}'>{countdown_text}</span>", unsafe_allow_html=True)
                    
                    # Add action buttons
                    button_col1, button_col2 = st.columns(2)
                    with button_col1:
                        if st.button(f"✏️ Edit", key=f"edit_{booking.get('id', i)}"):
                            st.session_state.edit_booking_id = booking.get('id')
                            st.info("Edit functionality would go here")
                    
                    with button_col2:
                        # Trigger cancel confirmation on button click
                        if st.button(f"❌ Cancel", key=f"cancel_{booking.get('id', i)}"):
                            st.session_state.show_cancel_confirmation = True
                            st.session_state.booking_to_cancel = booking
                            st.experimental_rerun()
    else:
        st.info("📭 You have no active bookings.")
        if st.button("🔍 Browse Available Trips", key="browse_trips_button"):
            st.session_state.menu_choice = "Trip Scheduling & Booking"
            st.experimental_rerun()
    
    # Cancel confirmation dialog
    if st.session_state.show_cancel_confirmation and st.session_state.booking_to_cancel:
        booking = st.session_state.booking_to_cancel
        
        # Display confirmation dialog
        st.markdown("---")
        st.warning("⚠️ **Cancel Booking Confirmation**")
        st.write(f"Are you sure you want to cancel your trip to **{booking['destination']}** on **{booking['date']}**?")
        
        # Cancellation policy information
        st.info("""
        **Cancellation Policy:**
        - Cancellations more than 30 days before departure: 85% refund
        - Cancellations 15-30 days before departure: 50% refund
        - Cancellations less than 15 days before departure: 25% refund
        - Cancellations on the day of departure: No refund
        """)
        
        # Calculate refund amount based on days until launch
        launch_date = datetime.datetime.strptime(booking['date'], "%Y-%m-%d")
        days_until_launch = (launch_date - datetime.datetime.now()).days
        
        if days_until_launch > 30:
            refund_percentage = 85
        elif days_until_launch >= 15:
            refund_percentage = 50
        elif days_until_launch > 0:
            refund_percentage = 25
        else:
            refund_percentage = 0
            
        refund_amount = (booking['price'] * refund_percentage) / 100
        
        st.write(f"**Estimated Refund:** ${refund_amount:,.2f} ({refund_percentage}% of ${booking['price']:,})")
        
        # Confirm or cancel buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔙 Go Back", key="go_back_button"):
                st.session_state.show_cancel_confirmation = False
                st.session_state.booking_to_cancel = None
                st.experimental_rerun()
                
        with col2:
            if st.button("✅ Confirm Cancellation", key="confirm_cancel_button"):
                try:
                    # Delete booking from Supabase
                    booking_id = booking.get('id')
                    response = supabase.table("bookings").delete().eq("id", booking_id).execute()
                    
                    if hasattr(response, "data") and response.data:
                        # Reset the confirmation dialog
                        st.session_state.show_cancel_confirmation = False
                        st.session_state.booking_to_cancel = None
                        
                        # Add to cancellation history table (optional)
                        cancellation_data = {
                            "user_email": current_user,
                            "destination": booking['destination'],
                            "original_date": booking['date'],
                            "class": booking['class'],
                            "original_price": booking['price'],
                            "refund_amount": refund_amount,
                            "cancellation_date": str(datetime.datetime.now().date())
                        }
                        
                        # Insert into cancellations table (if you have one)
                        try:
                            supabase.table("cancellations").insert(cancellation_data).execute()
                        except Exception:
                            # If cancellations table doesn't exist, just continue
                            pass
                            
                        st.success("✅ Your booking has been successfully cancelled. Any applicable refund will be processed within 5-7 business days.")
                        time.sleep(2)  # Give user time to read the message
                        st.experimental_rerun()
                    else:
                        st.error("⚠️ There was an error cancelling your booking. Please try again or contact customer support.")
                
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")
        
    # AI Travel Tips Section with improved styling
    st.markdown("---")
    st.subheader("🤖 AI Travel Tips")
    
    # Random tip selection for more variety
    tips = [
        "To prepare for zero-gravity, practice floating in water! 💧",
        "Pack light! Every gram counts when traveling to space. 🧳",
        "Space sickness is common - consider anti-nausea medication for your journey. 💊",
        "Stay hydrated! Water is precious in space travel. 🚰",
        "Bring a camera with extra memory cards - the views are unforgettable! 📸"
    ]
    
    st.info(random.choice(tips))
    
    # Add upcoming events or promotions
    st.markdown("### 🌠 Upcoming Events")
    events_col1, events_col2 = st.columns(2)
    
    with events_col1:
        st.write("**Mars Colony Grand Opening**")
        st.write("April 15, 2025")
        st.write("Special inaugural rates available!")
    
    with events_col2:
        st.write("**Solar Eclipse Viewing from Space**")
        st.write("May 22, 2025")
        st.write("Limited seats available!")

