import csv
import time
import os
# import readline # to be implemented for command history 4 previous tasks etc.
# import difflib # to recognize typos and suggest corrections

def tostr(t):
    return str(t).zfill(2)

class Item():
    def __init__(self):
        self.name = ""
        self.start = "00:00"
        self.end = "00:00"
        
    def prompt_name(self, prompt):
        self.name = input(prompt)
        if self.name == '':
            print("Please enter a name")
            self.prompt_name(prompt)
        
    def prompt_start(self, prompt):
        t = input(prompt)
        if t == '':
            now = time.localtime()
            t = tostr(now.tm_hour)+":"+tostr(now.tm_min)
        elif len(t) != 5: # check for format
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_start(prompt)
            return False # To end the current branch, otherwise becomes a tail-call
        try: # check for valid time
            time.strptime(t, "%H:%M")
        except ValueError:
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_start(prompt)
            return False # To end the current branch, otherwise becomes a tail-call

        self.start = t

    def prompt_end(self, prompt):
        t = input(prompt)
        if t == '':
            i = input("Type in 'end' to stop timer... ")
            while i == '' or i: # essentialy while True
                if i == "end":
                    now = time.localtime()
                    t = tostr(now.tm_hour)+":"+tostr(now.tm_min)
                    break
                else:
                    i = input("Type in 'end' to stop timer... ")
        elif len(t) != 5:
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_end(prompt)
            return False
        try: # check for valid time
            time.strptime(t, "%H:%M")
        except ValueError:
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_end(prompt)
            return False

        self.end = t

    def display(self):
        print("Item name: " + self.name + " was started at " + self.start + " and ended at " + self.end)
        # convert string to time.struct_time
        t1 = time.strptime(self.start, "%H:%M")
        t2 = time.strptime(self.end, "%H:%M")
        dif = time.mktime(t2)-time.mktime(t1)
        if dif < 0:
            dif+=60*60*24
        print("Elapsed time " + str(dif/60) + " minutes.")


def export_to_csv(*items):
    now = time.localtime()
    filename = str(now.tm_year)+tostr(now.tm_mon)+tostr(now.tm_mday)+'.csv'
    present = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        fieldnames = ['item_name', 'start_time', 'end_time']
        iw = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
        if not present:
            iw.writeheader()
        for i in items:
            iw.writerow({'item_name': i.name,
                        'start_time': i.start,
                         'end_time': i.end})

if __name__ == "__main__":
    i = Item()
    i.prompt_name("Name of the item: ")
    i.prompt_start("Enter start time: (blank for current) ")
    i.prompt_end("Enter end time: (blank for timer) ")
    i.display()
    export_to_csv(i)

    while input("Do you want to enter another item?(yY): ").lower() == 'y':
        i = Item()
        i.prompt_name("Name of the item: ")
        i.prompt_start("Enter start time: (blank for current) ")
        i.prompt_end("Enter end time: (blank for timer) ")
        i.display()
        export_to_csv(i)
