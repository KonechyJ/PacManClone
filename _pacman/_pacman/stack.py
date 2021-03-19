
#Class for stack objects and all the functions needed
class Stack(object):
    def __init__(self):
        self.items = []

    #method to check if the list is empty and returns a bool
    def isEmpty(self):
        if len(self.items) > 0:
            return False
        return True

    #clears out the list just in case
    def clear(self):
        self.items = []

    #adds an item to the end of the list
    def push(self):
        self.items.append(item)

    #removes an item from the end of the list (or the top of it)
    def pop(self):
        if not self.isEmpty():
            removedItem = self.items.pop(len(self.items)-1)
            return removedItem
        return None

    #This function allows us to see the next item to be taken off the top of the list without altering it
    def peeK(self):
        if not self.isEmpty():
            return self.items[len(self.items)-1]
        return None