import os
import streamlit as st

st.set_page_config(page_title="My Library Manager", page_icon="📚")

st.markdown("""
  <style>
    .main-container {
        max-width: 80%;
        margin: auto;
        transition: max-width 0.2s ease-in-out;
    }
    .stApp, .css-1v0mbdj, .css-ffhzg2, .css-1d391kg, .css-qrbaxs, .css-10trblm {
        color: white !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: white !important;
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>input,
    .stSelectbox>div>div>div,
    .stRadio>div>label {
        color: black !important;
    }
    section[data-testid="stSidebar"] {
        color: white !important;
    }
    .sidebar-hidden .main-container {
        max-width: 100%;
    }
    .css-1d391kg {
        padding: 2rem !important;
    }
    /* Background Gradient */
    .stApp {
        background: linear-gradient(to right, #04364A, #176B87);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #176B87, #64CCC5);
        color: black !important;
    }
    .stButton > button {
        background-color: #04364A;
        color: white !important;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        border: 2px solid #64CCC5;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #176B87;
        color: #64CCC5 !important;
        border-color: #04364A;
    }
    .stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(100, 204, 197, 0.4);
    }
  </style>
""", unsafe_allow_html=True)

# Load Library
def load_library(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return [
                {
                    'title': t,
                    'author': a,
                    'year': int(y),
                    'genre': g,
                    'read': r.lower() == 'true'
                }
                for line in file
                for t, a, y, g, r in [line.strip().split('|')]
            ]
    return []

# Save Library
def save_library(filename, books):
    with open(filename, 'w') as file:
        for b in books:
            file.write(f"{b['title']}|{b['author']}|{b['year']}|{b['genre']}|{b['read']}\n")

# Add a Book
def add_book(books):
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title:")
    author = st.text_input("Author:")
    year = st.number_input("Year Published:", min_value=1, step=1)
    genre = st.text_input("Genre:")
    read = st.radio("Read?", ["Yes", "No"])
    
    if st.button("Add Book 📥"):
        if title and author and genre:
            books.append({
                'title': title,
                'author': author,
                'year': year,
                'genre': genre,
                'read': read == "Yes"
            })
            save_library('library.txt', books)
            st.success(f"✅ '{title}' added to your library.")
        else:
            st.error("❗ All fields must be filled.")

# Remove Book
def remove_book(books):
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the title to remove:")
    if st.button("Remove Book"):
        for book in books:
            if book['title'].lower() == title.lower():
                books.remove(book)
                save_library('library.txt', books)
                st.success(f"✅ Removed '{title}'.")
                return
        st.error("❗ Book not found.")

# Search Books
def search_books(books):
    st.subheader("🔍 Search Books")
    search_by = st.selectbox("Search By:", ["Title", "Author"])
    keyword = st.text_input("Enter your search:")

    if st.button("Search"):
        matches = [
            b for b in books if keyword.lower() in b[search_by.lower()].lower()
        ]
        if matches:
            st.write("📘 Results:")
            for i, b in enumerate(matches, 1):
                status = "✅ Read" if b['read'] else "❌ Unread"
                st.write(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {status}")
        else:
            st.info("No matching books found.")

# Show All Books
def display_books(books):
    st.subheader("📖 Your Library")
    if books:
        for i, b in enumerate(books, 1):
            status = "✅ Read" if b['read'] else "❌ Unread"
            st.write(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {status}")
    else:
        st.info("No books added yet.")

# Stats
def display_statistics(books):
    st.subheader("📊 Stats")
    total = len(books)
    read = sum(1 for b in books if b['read'])
    percent = (read / total * 100) if total else 0

    st.write(f"📚 Total Books: {total}")
    st.write(f"✅ Read: {read}")
    st.write(f"📈 Completion: {percent:.2f}%")

#  Main App
def main():
    filename = 'library.txt'
    books = load_library(filename)

    st.title("📚 My Library Manager")
    
    menu = [
        "Add a Book", 
        "Remove a Book", 
        "Search for a Book", 
        "Display All Books", 
        "Display Statistics", 
        "Exit"
    ]
    choice = st.sidebar.radio("📋 Menu", menu)

    if choice == "Add a Book":
        add_book(books)
    elif choice == "Remove a Book":
        remove_book(books)
    elif choice == "Search for a Book":
        search_books(books)
    elif choice == "Display All Books":
        display_books(books)
    elif choice == "Display Statistics":
        display_statistics(books)
    elif choice == "Exit":
        save_library(filename, books)
        st.success("💾 Library saved. Goodbye!")

    st.markdown("""
    <hr style="margin-top: 2rem; margin-bottom: 1rem;">
    <p style="text-align:center; font-size:14px;">Built with ❤️ by Haris</p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
