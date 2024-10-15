tasks = []

def addTask():
    task = input("Please enter a task: ")
    tasks.append(task)
    print(f"Task '{task}' added to the list.")

def listTasks():
    if not tasks:
        print("There is no tasks currently.")
    else:
        print("Current Tasks:")
        for index, task in enumerate(tasks):
            print(f"Task #{index}. {task}")

def deleteTask():
    listTasks()  # Display current tasks
    while True:
        print("\n##. Go back to Main Menu")
        try:
            taskToDelete = input("Enter the task number to remove or '##' to go back: ")

            if taskToDelete == '##':
                print("Returning to Main Menu...")
                return  # Go back to main menu

            taskToDelete = int(taskToDelete)  # Convert input to an integer
            if taskToDelete >= 0 and taskToDelete < len(tasks):
                removed_task = tasks.pop(taskToDelete)  # Remove the task
                print(f"Task '{removed_task}' has been removed.")
            else:
                print(f"Task #{taskToDelete} was not found.")
        except ValueError:
            print("Invalid input. Please enter a valid task number or '##' to go back.")

             

if __name__ == "__main__":
    ###Create a loop to run the app
    print("Welcome to the to do list app")
    while True:
        print("\n")
        print("Please select one of the following options")
        print("------------------------------------------")
        print("1. Add a new task")
        print("2. Delete a task")
        print("3. List task")
        print("4. Quit")
        

        choice = input("Enter your choice: ")
    
        if (choice == "1"):
            addTask()
        elif(choice == "2"):
            deleteTask()
        elif(choice == "3"):
            listTasks()
        elif(choice == "4"):
            break
        else:
            print("Invalid input. Please try again.")
        
print("Goodbye!")