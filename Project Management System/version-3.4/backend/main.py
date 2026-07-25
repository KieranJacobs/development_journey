# main.py\version-3.4\

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
        project_ops.project_statistics()
    
    elif user_input == "10":
        project_ops.search_projects()

    elif user_input == "11":
        project_ops.view_high_priority_tasks()

    elif user_input == "12":
        project_ops.view_completed_tasks()

    elif user_input == "13":
        print("\nClosing Program.")
        break

    else:
        print("\nINVALID OPTION CHOSEN!\n")