from datetime import date
import time
import json

all_tasks = []

class task:
    def __init__(self, name, id, deadline = 365, requirements = []):
        self.is_completed = False
        self.name = name
        self.deadline = date.fromtimestamp(time.time() + deadline*60*60*24)
        self.requirements = requirements
        self.listeners = []
        self.doable = (requirements == [])
        self.id = id
        for req in requirements:
            get_task_by_id(req).add_listener(self)
        all_tasks.append(self)

    def add_listener(self, task):
        self.listeners.append(task)

    def complete_task(self):
        self.is_completed = True
        for listener in self.listeners:
            listener.requirements.remove(self.id)
            if (listener.requirements == []):
                listener.doable = True

def get_task_by_id(id):
    for task in all_tasks:
        if task.id == id:
            return task

def task_from_json(data):
    month, day = str.split(data["deadline"])
    deadline = (int(month)-int(date.today().strftime("%m")))*31 + (int(day)-int(date.today().strftime("%d")))
    return task(data["name"], data["id"], deadline=deadline, requirements = data["requirements"])

def make_test_graph():
    file = open("tasks.json")
    tasks = json.load(file)
    task1 = task_from_json(tasks[0])
    task2 = task_from_json(tasks[1])
    task3 = task_from_json(tasks[2])
    task1.complete_task()
    return [task1, task2, task3]

def print_pretty(graph) :
    for elt in graph:
        print(elt.name + " : A faire avant le " + elt.deadline.strftime("%m") + " " + elt.deadline.strftime("%d") + ", Faisable : " + str(elt.doable) + ", conditions = ", elt.requirements)

if __name__ == '__main__':
    graph = make_test_graph()
    print_pretty(graph)
