def menu_function():
    print()
    print("====== //                         // ======")
    print("====== / PROJECT MANAGEMENT SYSTEM / ======")
    print("         1. Create a Project               ")
    print("         2. Add a Task                     ")
    print("         3. Change Project Name/Title      ")
    print("         4. Change Project Status          ")
    print("         5. Delete a Project               ")
    print("         6. View all Projects              ")
    print("         7. Toggle Task Completion         ")
    print("         8. Delete a Task                  ")
    print("         9. View Project Statistics        ")
    print("        10. Search Projects by Name        ")
    print("        11. Filter Tasks (High Priority)   ")
    print("        12. Filter Tasks (Completed)       ")
    print("        13. Close Program                  ")
    print("====== //                         // ======")
    print()

def header(title):
    print()
    print("====== //                         // ======")
    print(f"====== / {title:^25} / ======")
    print("====== //                         // ======")
    print()

def priority_menu():
    print("===================================")
    print("====== // PRIORITY LEVELS // ======")
    print("===================================")
    print("1. High")
    print("2. Moderate")
    print("3. Low")
    print()

def status_menu():
    print("Possible Statuses: ")
    print("1. In Progress")
    print("2. Completed")
    print()

def get_valid_status():
    status_menu()
    while True:
        choice = input("Enter a new status for the project (1 or 2): ").strip()
        if choice == "1":
            return "In Progress"
        elif choice == "2":
            return "Completed"
        else:
            print("ERROR: INCORRECT STATUS CHANGE OPTION!\n")

def get_valid_priority():
    priority_menu()
    while True:
        choice = input("Select a Priority level for this task (1, 2, or 3): ").strip()
        if choice == "1":
            return "High"
        elif choice == "2":
            return "Moderate"
        elif choice == "3":
            return "Low"
        else:
            print("ERROR: INVALID PRIORITY LEVEL SELECTED!\n")