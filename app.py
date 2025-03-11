import streamlit as st  # Streamlit for creating the web-based UI
import re  # Regular expressions for pattern matching (useful for password validation)
import random  # Random module for generating passwords with random characters
import string  # String module for handling ASCII letters, digits, and punctuation

def check_password_strength(password): 
    score = 0  # Initialize password strength score
    suggestion = []  # List to store improvement suggestions
    # Length Check (Minimum 8 characters for better security)
    if len(password) >= 8:
        score += 1  # +1 point if password is 8+ characters long
    else:
        suggestion.append("❌ Password should be at least 8 characters long.")
    # Uppercase Letter Check (Enhances complexity)
    if re.search(r"[A-Z]", password):  # Regex checks for at least one uppercase letter
        score += 1
    else:
        suggestion.append("❌ Include uppercase letters.")
    # Lowercase Letter Check (Ensures letter variety)
    if re.search(r"[a-z]", password):  # Regex checks for at least one lowercase letter
        score += 1
    else:
        suggestion.append("❌ Include lowercase letters.")
    # Digit Check (Improves security by requiring numbers)
    if re.search(r"\d", password):  # Regex checks for at least one digit (0-9)
        score += 1
    else:
        suggestion.append("❌ Add at least one number (0-9).")
    # Special Character Check (Adds more randomness)
    if re.search(r"[-!@#$%^&*()_+=;:,.<>?/~]", password):  # Ensures presence of at least one special character
        score += 1
    else:
        suggestion.append("❌ Include at least one special character (!@#$%^&*).")
    return score, suggestion  # Returns strength score (0-5) and improvement suggestions



def generate_password(length):  # Random Password Generation Function
    # Define a set of special characters to be used in the password
    special_chars = "!@#$%^&*()_+=-;:,.<>?/~"
    # Ensuring at least one character from each category:
    password = [
        random.choice(string.ascii_lowercase),  # At least one lowercase letter (a-z)
        random.choice(string.ascii_uppercase),  # At least one uppercase letter (A-Z)
        random.choice(string.digits),           # At least one digit (0-9)
        random.choice(special_chars)            # At least one special character (!@#$...)
    ]
    # Fill the rest of the password with a mix of all character types
    password += random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + special_chars, k=length-4  ) # Remaining characters to reach the desired length
    random.shuffle(password)  # Shuffle to avoid predictable patterns
    return ''.join(password)  # Convert the list to a string and return it


def generate_ai_password(): # AI-Powered Password Generation Function
    """
    Simulating AI-powered password generation.
    You can replace this with an actual AI model in the future.
    """
    # 🔹 List of security-related words to make the password more meaningful
    security_words = ["Secure", "Strong", "Shield", "Encrypt", "Key", "Safe", "Vault", "Fortress","Guardian", "Cyber", "Lock", "Passcode", "Firewall", "Defense", "Privacy","Cipher", "Stealth", "Protector", "Intrusion", "Secrecy", "Sentinel", "Safeguard"]
    # Randomly select one word from the list
    word = random.choice(security_words)
    # Randomly mix upper and lower case letters in the selected word
    word = ''.join(random.choice([char.upper(), char.lower()]) for char in word)
    # Generate a random 4-digit number
    numbers = str(random.randint(1000, 9999))
    # Pick a random special character to add complexity
    special_chars = random.choice("!@#$%^&*()_+=-;:,.<>?/~")
    # Concatenate the parts to form the final password
    return word + numbers + special_chars  



# Main Function to Run The APP
def main():

    # Set page title and favicon
    st.set_page_config(page_title='Password Manager', page_icon='🔒')
    st.link_button("🔹 Created by Hammad Sheikh", "https://www.linkedin.com/in/hammad-sheikh-51294b284/")
    st.title("Password Manager 💻🔒")
    # Initialize session state
    if "password_history" not in st.session_state:
        st.session_state.password_history = {"strength": [], "random": [], "ai": []}

    # Sidebar navigation
    tab = st.sidebar.radio("Navigation", ["Password Strength Meter", "Generate Random Password", "Generate AI Password" , "Tips to Create Strong Passwords"])


# Password Strength Meter Tab
    if tab == "Password Strength Meter":
        # 🔹 Display section header
        st.header("🔒 Password Strength Meter")
        st.markdown("#### Enter your password to check its strength.")
        # 🔹 User input field for password (hidden for security)
        password = st.text_input("Enter Your Password", type="password")
        # 🔹 Button to check the strength of the entered password
        if st.button("Check Password Strength"):
            if password:  # Ensure password is not empty
                # 🔹 Call function to evaluate password strength (returns a score and suggestions)
                score, suggestion = check_password_strength(password)
                # 🔹 Provide feedback based on strength score
                if score <= 2:
                    st.error("❌ Weak Password")  # 🚨 Weak password warning
                elif score <= 4:
                    st.warning("⚠️ Moderate Password")  # ⚠️ Medium strength warning
                else:
                    st.success("✅ Strong Password!")  # ✅ Strong password confirmation
                # 🔹 Display numerical strength score
                st.write(f"Your password strength score is: {score}/5")
                # 🔹 Visual progress bar to indicate strength (scaled from 0 to 1)
                st.progress(score / 5)
                # 🔹 If suggestions are available, display them to the user
                if suggestion:
                    st.subheader("Suggestions to improve your password:")
                    for res in suggestion:
                        st.markdown(f"- {res}")  # 📝 Show each suggestion as a bullet point
                # 🔹 Store checked passwords in session history for reference
                st.session_state.password_history["strength"].append(password)
            else:
                st.error("Please enter a password to check its strength.")  # ❌ Error for empty input
        st.divider()
        # Show password history
        if st.session_state.password_history["strength"]:
            st.subheader("📜 Checked Password History")
            st.write("Here are your recently checked passwords:")
            for i, password in enumerate(reversed(st.session_state.password_history["strength"][-10:]), 1):
                st.code(password)



# Generate Random Password Tab
    elif tab == "Generate Random Password":
        st.header("🔑 Generate a Random Password")
        st.markdown("#### Struggling to create a strong password? Let us generate one for you!")
        length = st.number_input("Enter password length to generate:", min_value=8, max_value=16, step=1)
        # Generate Random Password 
        if st.button("Generate Password"):
            random_password = generate_password(length)
            st.session_state.password_history["random"].append(random_password)
            st.write("✅ Use this password for better security. Save it somewhere safe!")
            st.success(f"Your random password is: **{random_password}")
            st.code(random_password, language="plaintext")
        st.divider()
         # Show password history
        if st.session_state.password_history["random"]:
            st.subheader("📜 Random Password History")
            for i, password in enumerate(reversed(st.session_state.password_history["random"][-10:]), 1):
                st.code(password)



# Generate AI Password Tab
    elif tab == "Generate AI Password":
        st.header("🤖 Generate an AI-Powered Password")
        st.markdown("#### Let the AI create a strong password for you!")
        # Generate AI Password
        if st.button("Generate AI Password"):
            ai_password = generate_ai_password()
            st.session_state.password_history["ai"].append(ai_password)
            st.success(f"Your AI-generated password is: **{ai_password}**")
            st.code(ai_password, language="plaintext")
            st.write("✅ Use this password for better security. Save it somewhere safe!")

        st.divider()
        # Show password history
        if st.session_state.password_history["ai"]:
            st.subheader("📜 AI-Generated Password History")
            for i, password in enumerate(reversed(st.session_state.password_history["ai"][-10:]), 1):
                st.code(password)

    

# Tips to Create Strong Passwords Tab
    elif tab == "Tips to Create Strong Passwords":
        st.header("🔐 Tips to Create Strong Passwords")
        st.markdown("#### Here are some tips to create a strong password:")
        st.markdown("""
        - **Length**: Use passwords with 8 characters or more.
        - **Complexity**: Include a mix of letters, numbers, and symbols.
        - **Avoid Reusing**: Don't reuse passwords across different accounts.
        - **Password Manager**: Use a password manager to store your passwords securely.
        - **Two-Factor Authentication (2FA)**: Enable 2FA for an extra layer of security.
        - **Avoid Common Passwords**: Don't use common passwords like 'password123', 'qwerty', etc.
        - **Change Regularly**: Change your passwords regularly to keep your accounts secure.
        """)


# Run the app
if __name__ == "__main__":
    main()

    """
    🔹 Explanation
       1. __name__ is a special built-in variable in Python that holds the name of the current module.
       2. When a Python script is run directly, __name__ is set to "__main__", meaning it is the main program being executed.
       3. If the script is imported as a module into another script, __name__ will not be "__main__" but rather the module name.
    """
    """
    🔹 Example Usage
        1️⃣ When Running Directly
            If you run your Python file:

                python my_script.py
            __name__ will be "__main__", so main() will execute.

        2️⃣ When Importing as a Module
            If you import this script in another Python file:

                import my_script
            __name__ will be "my_script", not "__main__", so main() won’t execute automatically.
    """
