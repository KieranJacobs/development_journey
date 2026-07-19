library = [ 
    { 
        "bookTitle" : "book1",
        "author" : "John Doe",
        "genre" : "action",
        "status" : True
    },
    {
        "bookTitle" : "book2",
        "author" : "Jim Doe",
        "genre" : "sci-fi",
        "status" : False
    },
    {
        "bookTitle" : "book3",
        "author" : "Jane Doe",
        "genre" : "steampunk",
        "status" : False
    },
    {
        "bookTitle" : "book4",
        "author" : "Ben Doe",
        "genre" : "adventure",
        "status" : True
    }
]


def display_menu():
    print()
    print("====== // Personal Library Manager // ======")
    print("====== // Select an option // ======")
    print("1. View all books")
    print("2. Search by Title")
    print("3. Show unread books")
    print("4. Add a new book")
    print("5. Show Statistics")
    print("6. Quit")
    print("========== // // ==========")
    print()

def view_books():
    print()
    print("====== All Books ======")
    for book in library:
        print(f"Title: {book['bookTitle']}")
        print(f"Author: {book['author']}")
        print(f"Genre: {book['genre']}")
        print(f"is Read?: {book['status']}")
        print()
    

def search_book():
    print()
    searchTitle = input("Input a valid Book Title: ")
    found = False
    for book in library:
        if book["bookTitle"] == searchTitle:
            found = True
            print("====== // Search Results // ======")
            print(f"Title: {book['bookTitle']}")
            print(f"Author: {book['author']}")
            print(f"Genre: {book['genre']}")
            print(f"is Read?: {book['status']}")
    if not found:
        print("INVALID BOOK TITLE!")
    print()

def unread_books():
    for unread in library:
        if not unread["status"]:
            print("====== // Unread Books // ======")            
            print(f"Title: {unread['bookTitle']}")
            print(f"Author: {unread['author']}")
            print(f"Genre: {unread['genre']}")
            print(f"is Read?: {unread['status']}")

def add_book():
    print()
    print("====== // Input new Book Data // ======")
    title = input("Book Title: ")
    author = input("Author: ")
    genre = input("Genre: ")
    read_input = input("Read? (True/False): ")

    new_book = {
        "bookTitle" : title,
        "author" : author,
        "genre" : genre,
        "status" : read_input
    }

    library.append(new_book)
    print(library)
    print()

def show_stats():
    print()
    print("====== // Library Statistics // ======")
    book_Read = 0
    book_Unread = 0
    book_Count = len(library)
    for book in library:
        if book["status"]:
            book_Read += 1
        if not book["status"]:
            book_Unread += 1
    book_Percent = (book_Read / book_Count) * 100

    print(f"Total Books: {book_Count}")
    print(f"Total Books Read: {book_Read}")
    print(f"Total Books Unread: {book_Unread}")
    print(f"Total Percentage of Books Completed: {book_Percent}%")
    print()



while True:
    display_menu()

    userInput = input("Enter your chosen option here: ")

    if userInput == "1":
        view_books()
    
    elif userInput == "2":
        search_book()
    
    elif userInput == "3":
        unread_books()

    elif userInput == "4":
        add_book()

    elif userInput == "5":
        show_stats()

    elif userInput == "6":
        break
    
    else:
        print("INVALID OPTION CHOSEN!")
        break