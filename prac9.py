"""Simple Restaurant Chatbot
A basic chatbot that responds to customer queries about a restaurant.
"""

def get_response(user_input: str) -> str:
    """Match user input to predefined responses."""
    # Convert input to lowercase for easier matching
    user_input = user_input.lower()

    # Simple response dictionary
    responses = {
        "hello": "Hi! Welcome to our restaurant. How can I help you?",
        "hi": "Hi! Welcome to our restaurant. How can I help you?",
        "bye": "Goodbye! Have a nice day!",
        "menu": "We offer: \n- Pizza ($12)\n- Burger ($10)\n- Pasta ($15)\n- Salad ($8)",
        "hours": "We are open from 10 AM to 10 PM, Monday to Sunday.",
        "location": "We are located at 123 Main Street, Downtown.",
        "phone": "You can reach us at (555) 123-4567.",
        "delivery": "Yes, we offer delivery! Minimum order $20.",
        "payment": "We accept cash, credit cards, and digital payments.",
        "reservation": "To make a reservation, please call us at (555) 123-4567.",
        "wifi": "Yes, we have free WiFi for customers!",
        "parking": "Yes, free parking is available behind the restaurant."
    }

    # Check each keyword in the input
    for keyword in responses:
        if keyword in user_input:
            return responses[keyword]

    # Special cases for questions
    if "?" in user_input:
        return "Please call us at (555) 123-4567 for specific questions."

    # Default response
    return "I'm not sure about that. Can I help you with our menu, hours, location, or reservations?"


def chat():
    """Run the chatbot interaction."""
    print("Restaurant ChatBot")
    print("=" * 20)
    print("Type 'quit' to exit")
    print("Bot: Hi! How can I help you today?")

    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for quit
        if user_input.lower() == 'quit':
            print("Bot: Goodbye!")
            break

        # Get and print response
        response = get_response(user_input)
        print("Bot:", response)


if __name__ == "__main__":
    chat()
