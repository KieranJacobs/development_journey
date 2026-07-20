# main.py version-1

projects_list = []

def menu_function():
    print()
    print("====== //                         // ======")
    print("====== / PROJECT MANAGEMENT SYSTEM / ======")
    print("         1. Create a Project               ")
    print("         2. View all Projects              ")
    print("         3. Close Program                  ")
    print("====== //                         // ======")
    print()

def create_projects():
    print()
    print("====== //                         // ======")
    print("====== /   CREATE: A NEW PROJECT   / ======")
    print("====== //                         // ======")
    print()
    pname = input("Project Name?: ").strip()
    new_project = {
        "title": pname,
        "status": "Not Started"
    }

    projects_list.append(new_project)
    print(f"\nProject '{pname}' created successfully.")
    print(projects_list)

def view_projects():
    print()
    print("====== //                         // ======")
    print("===== / VIEW: ALL EXISTING PROJECTS / =====")
    print("====== //                         // ======")
    print()
    print(projects_list)

while True:
    menu_function()
    user_input = input("Please Select a Number from the Menu: ")
    
    if user_input == "1":
        create_projects()
    
    elif user_input == "2":
        view_projects()
    
    elif user_input == "3":
        break

    else:
        print("ERROR: INVALID OPTION CHOSEN! CHOOSE A VALID OPTION! (1,2,3...)")