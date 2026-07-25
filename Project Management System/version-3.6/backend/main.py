# main.py\version-3.6\

import project_ops
import ui_helpers

while True:
    ui_helpers.main_menu()
    main_choice = input("Select a category (1-4): ").strip()
    
    if main_choice == "1":
        while True:
            ui_helpers.project_menu()
            p_choice = input("Select a Project option (1-6): ").strip()
            
            if p_choice == "1":
                project_ops.create_projects()
            elif p_choice == "2":
                project_ops.edit_projects()
            elif p_choice == "3":
                project_ops.change_status()
            elif p_choice == "4":
                project_ops.search_projects()
            elif p_choice == "5":
                project_ops.delete_projects()
            elif p_choice == "6":
                break
            else:
                print("\nINVALID OPTION!\n")

    elif main_choice == "2":
        while True:
            ui_helpers.task_menu()
            t_choice = input("Select a Task option (1-4): ").strip()
            
            if t_choice == "1":
                project_ops.add_task()
            elif t_choice == "2":
                project_ops.toggle_task_completion()
            elif t_choice == "3":
                project_ops.delete_task()
            elif t_choice == "4":
                break 
            else:
                print("\nINVALID OPTION!\n")

    elif main_choice == "3":
        while True:
            ui_helpers.views_menu()
            v_choice = input("Select a View option (1-6): ").strip()
            
            if v_choice == "1":
                project_ops.view_projects()
            elif v_choice == "2":
                project_ops.project_statistics()
            elif v_choice == "3":
                project_ops.view_high_priority_tasks()
            elif v_choice == "4":
                project_ops.view_completed_tasks()
            elif v_choice == "5":
                project_ops.export_project_to_csv()
            elif v_choice == "6":
                break
            else:
                print("\nINVALID OPTION CHOSEN!\n")

    elif main_choice == "4":
        print("\nClosing Program.")
        break 
        
    else:
        print("\nINVALID OPTION CHOSEN!\n")