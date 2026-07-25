# main.py\version-2.4\

import project_ops
import ui_helpers

while True:
    ui_helpers.menu_function()
    user_input = input("Please Select a Number from the Menu: ")
    
    if user_input == "1":
        project_ops.create_projects()
    
    elif user_input == "2":
        project_ops.add_task()
    
    elif user_input == "3":
        project_ops.edit_projects()
    
    elif user_input == "4":
        project_ops.change_status()

    elif user_input == "5":
        project_ops.delete_projects()
    
    elif user_input == "6":
        project_ops.view_projects()
    
    elif user_input == "7":
        project_ops.toggle_task_completion()

    elif user_input == "8":
        project_ops.delete_task()
        
    elif user_input == "9":
        print("\nClosing Program.")
        break

    else:
        print("\nINVALID OPTION CHOSEN!\n")