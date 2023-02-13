# Compulsary task 1

# import datetime module
import datetime

# import tabulate module
from tabulate import tabulate

def login():
    while True:
        # Ask user for username and password and store in corresponding variables
        username = input("Please enter your username\n")
        
        # check to see if username exists
        # if the username exists ask user for the password
        if not check_user(username):
            print("\nUsername not found")
            login()
        else:
            password = input("\nPlease enter your password\n")

            # Open the user.txt file and read all the lines
            file = open("user.txt", "r")
            lines = file.readlines()

            # Loop through the username and passwords stored in user.txt    
            for line in lines:
                temp = line.split(", ")
                u_name = temp[0]
                p_word = temp[1].strip("\n")
                
                # Check to see if username and passwords match and display corresponding message
                if username == u_name and password == p_word:
                    msg = "\nCorrect Username and Password"
                    break
                elif username == u_name and password != p_word:
                    msg = "\nIncorrect Password. Please try again.\n"
                    break
            
            file.close()

            # If the username and passwords match then quit the loop
            if username == u_name and password == p_word:
                break
            
        # Display the error message
        print(msg)

    # Display the success message
    print(msg)

    main_menu(username)

def main_menu(username):
    while True:
        #presenting the menu to the user
        input_msg = "a  - Adding a task\nva - View all tasks\nvm - View my tasks\ne  - Exit\n"

        # add in other menu options to the admin user
        if username == "admin":
            input_msg = "r  - Register User\nvs - View Statistics\ngr - Generate Reports\n" + input_msg

        # making sure that the user input is converted to lower case incase they have capslock on
        menu = input("\nSelect one of the following Options below:\n" + input_msg).lower()

        # if the admin clicks r then we call up reg_user to register a new user
        if menu == 'r' and username == "admin":
            reg_user(username)

        # If the admin clicks vs then it will call the view_stats function
        elif menu == "vs" and username == "admin":
            view_stats()

        # If the admin clicks gr then it will call the reports function.
        elif menu == "gr" and username == "admin":
            reports()

        # add a task
        elif menu == 'a':
            add_task(username)

        # view all tasks
        elif menu == 'va':
            view_all()

        # view users tasks
        elif menu == 'vm':
            view_mine(username)

        # exit the program
        elif menu == 'e':
            print('\nGoodbye!!!\n')
            exit()
        else:
            print("\nIncorrect choice, Please Try again")

def reg_user(username):
    # admin enters a new user and password and stores to coresponding variables
    new_username = input("\nPlease enter a new username:\n")

    # If the user already exists then display error message and revert to the main menu
    if check_user(new_username):
        print("\nUsername already exists")
        main_menu(username)

    # If the user exists then ask for a password and password confirmation
    else:
        password = input("\nPlease enter a new password:\n")
        pw_conf = input("\nPlease re-enter your password:\n")

        # Checks to see if passwords match and if so stores the new user to the user.txt file
        # If passwords aren't the same then relevant error message is displayed.
        if pw_conf == password:
            file = open("user.txt", "a")
            file.write(new_username + ", " + password + "\n")
            file.close()
            print("\nUser successfully added")
        else:
            print("\nPasswords don't match! Please try again.")
            reg_user(username)

# Checks to see if the user exists
def check_user(user):
    # Open the user.txt file and read all the lines
    file = open("user.txt", "r")
    lines = file.readlines()

    # Loop through the username and passwords stored in user.txt    
    for line in lines:
        temp = line.split(", ")
        u_name = temp[0]

        # Check to see if username matches
        if user == u_name:
            exists = True
            break
        else:
            exists = False

    file.close()

    # returns the value of exists
    return(exists)

# opens tasks.txt and user.txt and counts the number of lines in each
# displays how many tasks and users there are
def view_stats():
    file = open("tasks.txt", "r")
    num = len(file.readlines())
    print("\nTasks:\t" + str(num))
    file.close()

    file = open("user.txt", "r")
    num = len(file.readlines())
    print("Users:\t" + str(num) + "\n")
    file.close()

def reports():
    # store today's date in today
    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y")

# **********************************TASK OVERVIEW*********************************************

    # initialise tasks dictionary to store the tasks
    tasks = {"Task Total": 0, "Completed Tasks": 0, "Uncompleted Tasks": 0, "Overdue Tasks": 0, "Percentage Incomplete": 0, "Percentage Overdue": 0}

    # Open up tasks.txt and read all the lines
    file = open("tasks.txt", "r")
    lines = file.readlines()

    # count the amount of lines and set the value of Task Total
    tasks["Task Total"] = len(lines)

    # Loop through the lines
    for line in lines:

        # Make the lines into lists
        temp = line.strip()
        temp = temp.split(", ")

        # count completed tasks
        if temp[6] == "Yes":
            tasks["Completed Tasks"] += 1

        # count overdue tasks
        if temp[6] == "No" and temp[5] < today:
            tasks["Overdue Tasks"] += 1
    
    # add on these calculated keys and values to the tasks dictionary
    # calculates the uncompleted tasks
    tasks["Uncompleted Tasks"] = tasks["Task Total"] - tasks["Completed Tasks"]

    # calculates percentage incomplete and assigns the value to tasks["Percentage Incomplete"]
    if tasks["Uncompleted Tasks"] > 0:
        tasks["Percentage Incomplete"] = int(100 / (tasks["Task Total"] / tasks["Uncompleted Tasks"]))
    else:
        tasks["Percentage Incomplete"] = 0

    # calculates percentage overdue and assigns the value to tasks["Percentage Overdue"]
    if tasks["Overdue Tasks"] > 0:
        tasks["Percentage Overdue"] = int(100 / (tasks["Task Total"] / tasks["Overdue Tasks"]))
    else:
        tasks["Percentage Overdue"] = 0

    file.close()

    # open up taskoverview.txt in write mode.
    # iterate through the dictionary and write the keys and values to the taskoverview.txt file
    with open("task_overview.txt", "w") as file:
        # I referenced https://realpython.com/iterate-through-dictionary-python/ which helped me with iterating through the dictionary.
        for item in tasks.items():
            file.writelines(str(item[0]) + ", " + str(item[1]) + "\n")

# *******************************************USER OVERVIEW*************************************************
    # Open up user.txt
    # Read the lines and initialise the count variables
    with open("user.txt", "r") as file:
        lines = file.readlines()
        task_count = 0
        completed_count = 0
        incomplete_count = 0
        overdue_count = 0

        # initialise user_overview dictionary
        user_overview = {"Number of Users": len(lines), "Total Tasks": tasks["Task Total"]}

        # Loop throug the users
        for line in lines:
            # Make the lines into lists
            temp = line.strip()
            temp = temp.split(", ")
            
            # Open up the tasks.txt file as read only
            with open("tasks.txt", "r") as f:
                tasks = f.readlines()

                # Loop through the tasks and convert them into lists
                for task in tasks:
                    tmp = task.strip()
                    tmp = tmp.split(", ")
                    
                    # check to see if the assigned user is the same as the current user
                    # adjust task_count, completed_count, incomplete_count, overdue_count accordingly
                    if temp[0] == tmp[1]:
                        task_count += 1
                        if tmp[6] == "Yes":
                            completed_count += 1
                        else:
                            incomplete_count += 1
                            if tmp[5] < today:
                                overdue_count =+1

                # Add on the extra keys and values to the user_overview dictionary
                # Total number of assigned tasks for this user
                user_overview[temp[0] + " - assigned tasks:"] = task_count

                # % of the total amount to tasks assigned to this user
                if task_count > 0:
                    user_overview[temp[0] + " - % of total tasks:"] = int(100 / (user_overview["Total Tasks"] / task_count))
                else:
                    user_overview[temp[0] + " - % of total tasks:"] = 0
                
                # The percentage of the tasks assigned to that user that have been completed
                if completed_count > 0:
                    user_overview[temp[0] + " - % of assigned tasks completed:"] = int(100 / (task_count / completed_count))
                else:
                    user_overview[temp[0] + " - % of assigned tasks completed:"] = 0

                # The percentage of the tasks assigned to that user that must still be completed
                if overdue_count > 0:
                    user_overview[temp[0] + " - % of assigned tasks that must still be completed:"] = int(100 / (task_count / incomplete_count))
                else:
                    user_overview[temp[0] + " - % of assigned tasks completed:"] = 0

                # The total number of tasks that haven’t been completed and that are overdue.
                if overdue_count > 0:
                    user_overview[temp[0] + " - % of assigned tasks overdue:"] = int(100 / (task_count / overdue_count))
                else:
                    user_overview[temp[0] + " - % of assigned tasks overdue:"] = 0
                
                # put counter back to 0 for the next user in the loop
                task_count = 0
                completed_count = 0
                incomplete_count = 0
                overdue_count = 0

    # open up user_overview.txt in write mode
    # loop through the items in user_overview dictionary and write them to user_overview.txt
    with open("user_overview.txt", "w") as file:
        for item in user_overview.items():
            file.write(item[0] + ", " + str(item[1]) + "\n")

    # Initialise stats list
    stats = []
    
    # open up task_overview.txt as a read only file and read all the lines
    with open("task_overview.txt", "r") as file:
        lines = file.readlines()

        # loops through and converts each line to a list
        for line in lines:
            temp = line.strip()
            temp = temp.split(", ")

            # makes a list of the temp lists
            stats.append(temp)

    # Prints out the Task report in a table
    head = ["TASK STATS", ""]
    print(tabulate(stats, headers=head, tablefmt="grid"))

    # re-initialises the stats list
    stats = []
    
    # open up user_overview.txt as a read only file and read all the lines
    with open("user_overview.txt", "r") as file:
        lines = file.readlines()

        # loops through and converts each line to a list
        for line in lines:

            temp = line.strip()
            temp = temp.split(", ")

            # makes a list of the temp lists
            stats.append(temp)

    # Prints out the User report in a table
    head = ["USER STATS", ""]
    print(tabulate(stats, headers=head, tablefmt="grid"))

# This function compares the assigned date and due date and checks for errors and returns a message if there's a problem
def check_date(assigned_date, due_date):
    try:
        assigned = datetime.datetime.strptime(assigned_date, '%d-%m-%Y')
        datetime.datetime.strptime(due_date, '%d-%m-%Y')
        msg = "Correct Format"
        due = datetime.datetime.strptime(due_date, '%d-%m-%Y')
        if due >= assigned:
            msg = ""
        else:
            msg = "\nDue date cannot be before the Assigned date"
        return msg
    except:
        msg = "\nIncorrect Format"
        return msg

def add_task(username):
    # I referenced https://www.w3schools.com/python/python_datetime.asp to learn about dates in python
    # assigns the current datetime to now
    # stores todays date in today
    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y")

    # Get the data from the user aswell as the date and completed info and save the data to variables in preperation to add to tasks.txt
    user_name = input("Please enter the username of the person whom the task is assigned to:\n")

    # call check_user function to make sure that user exists
    if check_user(user_name):
        
        # asks user for the title and description and saves them to the corresponding variables
        title = input("Please enter the title of the task:\n")
        desc = input("Please enter the description of the task:\n")

        # asks user to enter the due date
        # check_date validates the date and returns back a message that is displayed to the user
        while True:
            due = input("Please enter the due date (dd-mm-yyyy):\n")
            print(check_date(today, due))
            
            # if there's no message then break out of the loop
            if check_date(today, due) == "":
                break
        
        # set the completed variable to No as default
        completed = "No"

        # Open tasks.txt
        # move filepoint to beginning with file.seek so we can count the lines from the beginning.
        # I got this info from https://mkyong.com/python/python-difference-between-r-w-and-a-in-open/#:~:text=The%20r%20means%20reading%20file,and%20writing%20file%2C%20append%20mode
        # Create an id by finding out how many lines and then adding 1 to create an id number for the new line.
        # Write the new data to tasks.txt and close the file
        file = open("tasks.txt", "a+")
        file.seek(0)
        lines = file.readlines()
        id = str((len(lines)) + 1)
        file.write(id + ", " + user_name + ", " + title + ", " + desc + ", " + today + ", " + due + ", " + completed + "\n")
        file.close()
        
        print("Successfully Added")

        view_all()

        main_menu(username)
    else:
        print("User doesn't exist")
        main_menu(username)

def edit_task(username, selected_task, f_index, new_val):
    # initialise user_task list
    user_task = []

    # open up tasks.txt in read + mode
    # read all the lines and assign the contents to lines.
    with open("tasks.txt","r+") as file:
        lines = file.readlines()

        # Loop through the lines
        for line in lines:
            # Make the lines into lists
            temp = line.strip()
            temp = temp.split(", ")

            # checks if the selected task number is the same as the id number of the current task
            if temp[0] == selected_task:
                # sets the new value for that the specified field (f_index) to new_val
                # concatonate all the temps and commas together and save in new_line to be written to the tasks.txt
                temp[f_index] = new_val
                new_line = temp[0] + ", " + temp[1] + ", " + temp[2] + ", " + temp[3] + ", " + temp[4] + ", " + temp[5] + ", " + temp[6] + "\n"

                # set the user_task to be passed into the task_table to be displayed
                user_task.append(temp)

    # calculates the number of lines in tasks.txt and assigns the value to num_lines
    num_lines = (len(lines))

    # open up tasks.txt in write mode
    # loops through and re-writes all of the tasks that haven't been altered.
    # then writes new_line which contains the edited value.
    with open("tasks.txt", "w") as file:
        for i in range (num_lines):
            if i != int(selected_task)-1:
                file.writelines(lines[i])
            else:
                file.writelines(new_line)

    # display success message
    # pass the user_task as an argument in task_table to display the edited field
    print("Successfully Updated")
    task_table(user_task)

    main_menu(username)
    
def view_all():
    # initialise display_tasks to store the tasks to be displayed in a table
    display_tasks = []

    # Open up tasks.txt and read all the lines
    file = open("tasks.txt", "r")
    lines = file.readlines()

    # Loop through the lines
    for line in lines:

        # Make the lines into lists
        temp = line.strip()
        temp = temp.split(", ")

        # add temp to the list of tasks to be displayed
        display_tasks.append(temp)

    # display table
    task_table(display_tasks)

    file.close()

def view_mine(username):
    # initialise user_tasks list to store selected ids of tasks for the user 
    user_tasks = []

    # initialise display_tasks to store the tasks to be displayed in a table
    display_tasks = []

    # Open up tasks.txt and read all the lines
    file = open("tasks.txt", "r")
    lines = file.readlines()
    file.close()

    # Loop through the lines
    for line in lines:

        # Make the lines into lists
        temp = line.strip()
        temp = temp.split(", ")

        # Check to see if the username logged and the username listed on tasks.txt match up
        if username == temp[1]:

            # create a list of id numbers of tasks that belong to that user
            user_tasks.append(temp[0])

            # add temp to the list of tasks to be displayed
            display_tasks.append(temp)

    # display table
    task_table(display_tasks)

    view_selected(username, user_tasks)

def task_table(display_tasks):
    # table headings
    head = ["ID", "ASSIGNED TO", "TASK", "DESCRIPTION", "DATE ASSIGNED", "DUE", "COMPLETE"]

    # display table
    print(tabulate(display_tasks, headers=head, tablefmt="grid"))

def view_selected(username, tasks):
    # initialise user_task list
    user_task = []
    # ask user for a task number and save the input into selected_task
    selected_task = input("\nPlease select a task number or type -1 to return to the main menu\n")

    # checks to make sure the selected task is on of their tasks and there are no errors in input
    if selected_task in tasks:
        print(f"\nYou have selected task number {selected_task}\n")
        # opens tasks.txt in read mode and reads the lines
        file = open("tasks.txt", "r")
        lines = file.readlines()
        file.close()

        # Loop through the lines
        for line in lines:
            # Make the lines into lists
            temp = line.strip()
            temp = temp.split(", ")

            # check to see if the selected task is the same as the task being looped through
            # send the user_task which was selected to task_table to be displayed
            if selected_task == temp[0]:
                assigned = temp[4]
                # assigned = datetime.datetime.strptime(assigned_date, '%d-%m-%Y')
                user_task.append(temp)
                task_table(user_task)
                break
        
        # call up make_a_choice where the user selects what they would like to do with the selected_task
        make_a_choice(username, selected_task, assigned)
    # if the user has chosen -1 it will take them back to main_menu
    elif selected_task == "-1":
        main_menu(username)
    else:
        # if the user has entered incorrectly it will give error message and take them back to view_selected
        print("\nIncorrect Input - not one of your tasks\n")
        view_selected(username, tasks)

def make_a_choice(username, selected_task, assigned):
    # ask the user what they would like to do next and store answer in choice variable
    choice = (input("\nWhat would you like to do next? \nc - Mark as complete\ne - Edit the task\nm - Return to the Main Menu\n"))

    # set default field_index to 6 which is the completed field
    field_index = 6

    # set the new_value to Yes to be passed if the user clicks on c - Mark as complete
    new_value = "Yes"

    # c - Mark as complete
    if choice.lower() == "c":
        edit_task(username, selected_task, field_index, new_value)
    # e - Edit the task
    elif choice.lower() == "e":
        # check to see if task has already been completed
        if check_complete(selected_task):
            print("Unable to edit - The task has already been completed")
            main_menu(username)
        else:
            # check to see which field the user wants to change and set the field_index accordingly
            # set new_value based on the input the user gives
            field_selection = input("\nWhich field would you like to change? \na  - Assigned to\ndd - Due Date\n")
            if field_selection == "a":
                field_index = 1
                new_value = input("\nPlease enter the new user:\n")
            elif field_selection == "dd":
                field_index = 5
                while True:
                    new_value = input("Please enter the due date (dd-mm-yyyy):\n")
                    # validate the date given
                    print(check_date(assigned, new_value))
                    
                    if check_date(assigned, new_value) == "":
                        break
            else:
                print("Incorrect input!")
                make_a_choice(username, selected_task)

        # pass over the username, the selected task, the field index of the selected task and the new value to be changed to edit_task.
        edit_task(username, selected_task, field_index, new_value)
    elif choice.lower() == "m":
        # if the user selects m then direct back to main menu
        main_menu(username)
    else:
        # error handling
        print("invalid choice! Please try again")
        make_a_choice(username, selected_task)

# check to see if the task has been completed and return True or False
def check_complete(selected):
    file = open("tasks.txt", "r")
    lines = file.readlines()
    file.close()

    # Loop through the lines
    for line in lines:
        # Make the lines into lists
        temp = line.strip()
        temp = temp.split(", ")

        # check to see if the selected task is the same as the on being looped through
        # send the user_task which was selected to task_table to be displayed
        if selected == temp[0]:
            if temp[6] == "Yes":
                completed = True
            else:
                completed = False
    
    # return true of false depending on whether the task has been completed or not.
    return(completed)

login()