import streamlit as st

def main_home():
    st.title('Favorit Hotel in Jawa Timur')
    st.header('Drasri Beautiful Luxury Hotel')
    
    # Add an image of the hotel
    image_path = "path/to/your/hotel_image.jpg"  # Replace with the actual path or URL
    st.image(image_path, caption='Drasri Beautiful Luxury Hotel', use_column_width=True)

    # Add any content for the main home page
    st.write("Welcome to Drasri Beautiful Luxury Hotel! Experience the epitome of comfort and luxury in the heart of Jawa Timur.")

    # You can add more content, sections, or styling here as needed
    st.markdown("---")  # Add a horizontal line for separation

    # Example: Add a section with styled text
    st.header("Our Services")
    st.write("Discover our exclusive services designed to make your stay memorable.")

    # Example: Add bullet points
    st.subheader("Services Include:")
    st.markdown("- Room service")
    st.markdown("- Spa and wellness facilities")
    st.markdown("- Concierge service")

    # Continue adding more content or sections as needed
