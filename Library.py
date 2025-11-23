# ---------------- Book class ----------------

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status  # "available" or "issued"

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"


# ------------- Inventory class --------------

class LibraryInventory:
    def __init__(self, filename="books.txt"):
        self.filename = filename
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        self.books.append(book)
        self.save_to_file()

    def search_by_title(self, title):
        title = title.lower()
        result = []
        for b in self.books:
            if title in b.title.lower():
                result.append(b)
        return result

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books in library.")
        else:
            for b in self.books:
                print(b)

    # ---------- file save / load with TXT ----------

    def save_to_file(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for b in self.books:
                    # title|author|isbn|status\n
                    line = f"{b.title}|{b.author}|{b.isbn}|{b.status}\n"
                    f.write(line)
        except Exception as e:
            print("Error saving file:", e)

    def load_from_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.books = []
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("|")
                    if len(parts) != 4:
                        continue  # skip bad lines
                    title, author, isbn, status = parts
                    book = Book(title, author, isbn, status)
                    self.books.append(book)
        except FileNotFoundError:
            # First time: file does not exist, this is OK
            self.books = []
        except Exception as e:
            print("Error loading file:", e)
            self.books = []


# ---------- Helper functions ----------

def add_book_menu(inventory):
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    isbn = input("Enter ISBN: ").strip()

    if not title or not author or not isbn:
        print("All fields are required.")
        return

    if inventory.search_by_isbn(isbn) is not None:
        print("Book with this ISBN already exists.")
        return

    book = Book(title, author, isbn)
    inventory.add_book(book)
    print("Book added.")


def issue_book_menu(inventory):
    isbn = input("Enter ISBN to issue: ").strip()
    book = inventory.search_by_isbn(isbn)
    if book is None:
        print("Book not found.")
        return
    if book.status == "issued":
        print("Book already issued.")
    else:
        book.status = "issued"
        inventory.save_to_file()
        print("Book issued.")


def return_book_menu(inventory):
    isbn = input("Enter ISBN to return: ").strip()
    book = inventory.search_by_isbn(isbn)
    if book is None:
        print("Book not found.")
        return
    if book.status == "available":
        print("Book is not issued.")
    else:
        book.status = "available"
        inventory.save_to_file()
        print("Book returned.")


def search_menu(inventory):
    print("1. Search by title")
    print("2. Search by ISBN")
    choice = input("Enter choice: ").strip()
    if choice == "1":
        title = input("Enter title: ").strip()
        results = inventory.search_by_title(title)
        if not results:
            print("No books found.")
        else:
            for b in results:
                print(b)
    elif choice == "2":
        isbn = input("Enter ISBN: ").strip()
        book = inventory.search_by_isbn(isbn)
        if book is None:
            print("No book found.")
        else:
            print(book)
    else:
        print("Invalid choice.")


# ---------- Main menu loop ----------

def main():
    inventory = LibraryInventory()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_book_menu(inventory)
        elif choice == "2":
            issue_book_menu(inventory)
        elif choice == "3":
            return_book_menu(inventory)
        elif choice == "4":
            inventory.display_all()
        elif choice == "5":
            search_menu(inventory)
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
