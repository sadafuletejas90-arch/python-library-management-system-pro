#=============================================================================================================
#Project Name: Library Management System Pro
#Author: Tejas Sadafule
#Language:Python
# Version: 2.0
#=============================================================================================================

import json
import json
import os

class LibrarySystem:
    def __init__(self, filename="library_data.json"):
        """Initializes the database file and loads existing records."""
        self.filename = filename
        self.data = {"books": {}, "members": {}}
        self.load_data()

    def load_data(self):
        """Loads data from the JSON file or creates a new file if absent."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.data = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                print("⚠️ Database corrupted or empty. Starting fresh. - library_management_system.py:26")
                self.save_data()
        else:
            self.save_data()

    def save_data(self):
        """Saves current memory state back to the JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_book(self, book_id, title, author):
        """Adds a unique book to the catalog."""
        if book_id in self.data["books"]:
            print(f"❌ Error: Book ID '{book_id}' already exists. - library_management_system.py:39")
            return
        
        self.data["books"][book_id] = {
            "title": title,
            "author": author,
            "is_borrowed": False,
            "borrowed_by": None
        }
        self.save_data()
        print(f"📚 Book '{title}' added successfully! - library_management_system.py:49")

    def add_member(self, member_id, name):
        """Registers a new library member."""
        if member_id in self.data["members"]:
            print(f"❌ Error: Member ID '{member_id}' already exists. - library_management_system.py:54")
            return

        self.data["members"][member_id] = {
            "name": name,
            "borrowed_books": []
        }
        self.save_data()
        print(f"👤 Member '{name}' registered successfully! - library_management_system.py:62")

    def list_books(self):
        """Displays all available and borrowed books."""
        if not self.data["books"]:
            print("📭 The library has no books currently. - library_management_system.py:67")
            return
        
        print("\n Library Catalog - library_management_system.py:70")
        for b_id, info in self.data["books"].items():
            status = f"Borrowed by {info['borrowed_by']}" if info["is_borrowed"] else "Available"
            print(f"ID: {b_id} | Title: {info['title']} | Author: {info['author']} | Status: {status} - library_management_system.py:73")

    def borrow_book(self, book_id, member_id):
        """Assigns an available book to a valid registered member."""
        if book_id not in self.data["books"]:
            print("❌ Error: Book ID not found. - library_management_system.py:78")
            return
        if member_id not in self.data["members"]:
            print("❌ Error: Member ID not found. - library_management_system.py:81")
            return
        if self.data["books"][book_id]["is_borrowed"]:
            print("❌ Error: Book is already checked out. - library_management_system.py:84")
            return

        # Update book state
        self.data["books"][book_id]["is_borrowed"] = True
        self.data["books"][book_id]["borrowed_by"] = member_id
        
        # Update member state
        self.data["members"][member_id]["borrowed_books"].append(book_id)
        
        self.save_data()
        print(f"📖 Book '{self.data['books'][book_id]['title']}' successfully issued to {self.data['members'][member_id]['name']}. - library_management_system.py:95")

    def return_book(self, book_id):
        """Returns a borrowed book back to the catalog inventory."""
        if book_id not in self.data["books"]:
            print("❌ Error: Book ID not found. - library_management_system.py:100")
            return
        if not self.data["books"][book_id]["is_borrowed"]:
            print("❌ Error: This book is already in the library. - library_management_system.py:103")
            return

        member_id = self.data["books"][book_id]["borrowed_by"]
        
        # Reset book status
        self.data["books"][book_id]["is_borrowed"] = False
        self.data["books"][book_id]["borrowed_by"] = None
        
        # Remove from member tracking list
        if member_id in self.data["members"]:
            self.data["members"][member_id]["borrowed_books"].remove(book_id)

        self.save_data()
        print("✅ Book returned safely! - library_management_system.py:117")

# --- Interactive Terminal UI ---
def main():
    lms = LibrarySystem()
    
    while True:
        print("\n=== Library Menu === - library_management_system.py:124")
        print("1. Add Book - library_management_system.py:125")
        print("2. Add Member - library_management_system.py:126")
        print("3. List All Books - library_management_system.py:127")
        print("4. Borrow Book - library_management_system.py:128")
        print("5. Return Book - library_management_system.py:129")
        print("6. Exit - library_management_system.py:130")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            b_id = input("Enter Book ID: ").strip()
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author Name: ").strip()
            if b_id and title and author:
                lms.add_book(b_id, title, author)
            else:
                print("⚠️ Fields cannot be empty. - library_management_system.py:141")
                
        elif choice == "2":
            m_id = input("Enter Member ID: ").strip()
            name = input("Enter Member Name: ").strip()
            if m_id and name:
                lms.add_member(m_id, name)
            else:
                print("⚠️ Fields cannot be empty. - library_management_system.py:149")
                
        elif choice == "3":
            lms.list_books()
            
        elif choice == "4":
            b_id = input("Enter Book ID to borrow: ").strip()
            m_id = input("Enter Member ID: ").strip()
            lms.borrow_book(b_id, m_id)
            
        elif choice == "5":
            b_id = input("Enter Book ID to return: ").strip()
            lms.return_book(b_id)
            
        elif choice == "6":
            print("👋 Exiting system. Goodbye! - library_management_system.py:164")
            break
        else:
            print("⚠️ Invalid choice. Please try again. - library_management_system.py:167")

if __name__ == "__main__":
    main()