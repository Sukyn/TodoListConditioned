from datetime import date
import time

class task:
    def __init__(self, name, deadline = 365, requirements = []):
        self.is_completed = False
        self.name = name
        self.deadline = date.fromtimestamp(time.time() + deadline*60*60*24)
        self.requirements = requirements
        self.listeners = []
        self.doable = (requirements == [])
        for req in requirements:
            req.add_listener(self)

    def add_listener(self, task):
        self.listeners.append(task)

    def complete_task(self):
        self.is_completed = True
        for listener in self.listeners:
            listener.requirements.remove(self)
            if (listener.requirements == []):
                listener.doable = True

def make_test_graph():
    task1 = task("cut my hair", deadline = 0)
    task2 = task("shave", deadline=2, requirements = [task1])
    task3 = task("eat", deadline=5, requirements = [task2, task1])
    task1.complete_task()
    return [task1, task2, task3]

def print_pretty(graph) :
    for elt in graph:
        print(elt.name + " : A faire avant le " + elt.deadline.strftime("%m") + " " + elt.deadline.strftime("%d") + ", Faisable : " + str(elt.doable) + ", conditions = ", elt.requirements)

if __name__ == '__main__':
    graph = make_test_graph()
    print_pretty(graph)
