class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
# Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py ls
# Delete the incomplete item with the given priority number
$ python tasks.py del PRIORITY_NUMBER
# Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py done PRIORITY_NUMBER
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        priority = int(args[0])
        task = args[1]

        def modifyPriority(priority):
            if priority+1 in self.current_items.keys():
                priority = priority+1
                modifyPriority(priority)
            else:
                self.current_items[priority+1] = self.current_items[priority]
                del self.current_items[priority]

        def addTaskWithPriority(priority, task):
            self.current_items[priority] = task
            self.write_current()
            print('Added task: "{}" with priority {}'.format(task, priority))

        def PriorityCheck(priority, task):
            while priority in self.current_items.keys():
                modifyPriority(priority)
            addTaskWithPriority(priority, task)

        PriorityCheck(priority, task)

    def done(self, args):
        priority = int(args[0])

        def addCompletedTask(task):
            self.completed_items.append(task)
            self.write_completed()

        if priority in self.current_items.keys():
            task = self.current_items[priority]
            addCompletedTask(task)
            del self.current_items[priority]
            self.write_current()
            print("Marked item as done.")
        else:
            print(
                f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        priority = int(args[0])
        if priority in self.current_items.keys():
            del self.current_items[priority]
            self.write_current()
            print(f"Deleted item with priority {priority}")
        else:
            print(
                f"Error: item with priority {priority} does not exist. Nothing deleted.")

    def ls(self):
        self.read_current()
        listString = []
        for index, priority in enumerate(sorted(self.current_items.keys())):
            listString.append(
                f"{index+1}. {self.current_items[priority]} {[priority]}\n")
        listString[len(listString) -
                   1] = listString[len(listString)-1].rstrip("\n")
        for listTask in listString:
            print(listTask, end="")

    def report(self):
        self.read_current()
        self.read_completed()
        pendingTaskCount = len(self.current_items)
        completedTaskCount = len(self.completed_items)
        pendingString = f"Pending : {pendingTaskCount}\n"
        completedString = f"Completed : {completedTaskCount}\n"
        for index, priority in enumerate(sorted(self.current_items)):
            pendingString = pendingString + \
                f"{index+1}. {self.current_items[priority]} {[priority]}\n"
        for index, task in enumerate(sorted(self.completed_items)):
            completedString = completedString + \
                f"{index+1}. {self.completed_items[index]}\n"
        finalString = pendingString+"\n"+completedString.rstrip("\n")
        print(finalString, end="")
