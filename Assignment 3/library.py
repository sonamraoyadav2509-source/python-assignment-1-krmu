class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status 

    def to_line(self):
        return self.title + "|" + self.author + "|" + self.isbn + "|" + self.status

    @staticmethod
    def from_line(line):
        parts = line.strip().split("|")
        if len(parts) != 4:
            return None
        return Book(parts[0], parts[1], parts[2], parts[3])

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"


class LibraryInventory:
    def __init__(self, filename="inventory.txt"):
        self.filename = filename
        self.books = []
        self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    book = Book.from_line(line)
                    if book:
                        self.books.append(book)
        except FileNotFoundError:
            try:
                open(self.filename, "w").close()
            except:
                print("Error: Could not create inventory file!")
        except Exception as e:
            print("Error reading inventory file:", e)

    def save_inventory(self):
        try:
            with open(self.filename, "w") as file:
                for book in self.books:
                    file.write(book.to_line() + "\n")
        except Exception as e:
            print("Error saving inventory file:", e)

    def add_book(self, title, author, isbn):
        if self.search_by_isbn(isbn): 
            return False
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_inventory()
        return True

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books


def menu():
    print("\n--- Library Inventory Manager ---")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book by Title")
    print("6. Exit")
    return input("Enter choice: ")


def main():
    inventory = LibraryInventory()

    while True:
        choice = menu()

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")

            if inventory.add_book(title, author, isbn):
                print("Book added successfully!")
            else:
                print("A book with this ISBN already exists.")

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)

            if book and book.issue():
                inventory.save_inventory()
                print("Book issued successfully!")
            else:
                print("Book not found or already issued.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)

            if book and book.return_book():
                inventory.save_inventory()
                print("Book returned successfully!")
            else:
                print("Book not found or already available.")

        elif choice == "4":
            books = inventory.display_all()
            if not books:
                print("No books in inventory.")
            else:
                print("\n--- All Books ---")
                for b in books:
                    print(
                        "Title:", b.title,
                        "| Author:", b.author,
                        "| ISBN:", b.isbn,
                        "| Status:", b.status
                    )

        elif choice == "5":
            title = input("Enter title to search: ")
            results = inventory.search_by_title(title)

            if results:
                print("\n--- Search Results ---")
                for b in results:
                    print(
                        "Title:", b.title,
                        "| Author:", b.author,
                        "| ISBN:", b.isbn,
                        "| Status:", b.status
                    )
            else:
                print("No books found with that title.")

        elif choice == "6":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
