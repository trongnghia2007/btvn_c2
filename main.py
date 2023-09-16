# Array implementation of a heap
# Function in here will directly modify the order of elemnents
# in the heap 
class max_heap_functions:
    # Convert a normal array into an array-based heap
    @staticmethod
    def heapify(arr):
        for i in range(len(arr) // 2, -1, -1):
            max_heap_functions.siftdown(arr, i)

    @staticmethod
    def siftup(heap, index):
        if index == 0:
            return
        parent = index // 2
        # if parent is smaller than child, swap them
        if heap[parent] < heap[index]:
            heap[parent], heap[index] = heap[index], heap[parent]
            max_heap_functions.siftup(heap, parent)
    
    @staticmethod
    def siftdown(heap, index):
        larger_child = index * 2
        # if this element doesn't have children then stop
        if larger_child >= len(heap):
            return
        # choose the larger child to compare
        if larger_child + 1 < len(heap) and heap[larger_child] < heap[larger_child + 1]:
            larger_child += 1
        # if child > parent, swap them
        if heap[index] < heap[larger_child]:
            heap[larger_child], heap[index] = heap[index], heap[larger_child]
            max_heap_functions.siftdown(heap, larger_child)
    
    # Add an element to the heap and maintain the heap property
    @staticmethod
    def add(heap, ele):
        heap.append(ele)
        max_heap_functions.siftup(heap, len(heap) - 1)
    
    # Remove the root of the heap and maintain the heap property
    @staticmethod
    def remove_root(heap):
        last = len(heap) - 1
        # Swap the root and the last element
        heap[0], heap[last] = heap[last], heap[0]
        root = heap.pop() # remove the last element (which is the root)
        max_heap_functions.siftdown(heap, 0)
        return root

class Teller:
    def __init__(self):
        self.customer = None
        self.times_served = 0
        self.duration_served = 0 
    def serve(self, customer, curr_time):
        self.customer = customer
        self.times_served += 1
        self.duration_served += customer.duration
        customer.actual_served_time = curr_time

    def finish_serving(self):
        self.customer = None
    
    def __eq__(self, other):
        return self is other
    def __lt__(self, other):
        return (self.customer.leave_time() > other.customer.leave_time()) 
    def __le__(self, other):
        return self == other or self < other
    def __gt__(self, other):
        return not (self <= other)
    def __ge__(self, other):
        return not (self < other)

class TellerManager:
    def __init__(self, tellers):
        self.tellers = tellers
        self.busy = []
        self.free = [teller for teller in tellers]

    def serve_customer(self, customer, curr_time):
        teller = self.free.pop(0)
        teller.serve(customer, curr_time)
        max_heap_functions.add(self.busy, teller)
    
    def finish_earliest_service(self):
        teller = max_heap_functions.remove_root(self.busy)
        teller.finish_serving()
        self.free.append(teller)
    
    def earliest_service_end(self):
        if self.busy:
            return self.busy[0].customer.leave_time()
        else:
            return None 

class Customer:
    def __init__(self, arrive_time, duration, priority):
        self.arrive_time = arrive_time
        self.duration = duration
        self.priority = priority
        self.actual_served_time = None
    def wait_time(self):
        return self.actual_served_time - self.arrive_time
    def leave_time(self):
        return self.actual_served_time + self.duration

    def __eq__(self, other):
        return self is other
    def __lt__(self, other):
        return (self.priority < other.priority) or (self.arrive_time > other.arrive_time) 
    def __le__(self, other):
        return self == other or self < other
    def __gt__(self, other):
        return not (self <= other)
    def __ge__(self, other):
        return not (self < other)
    def __str__(self):
        return f"Customer({self.arrive_time}, {self.duration}, {self.priority})"

class CustomerManager:
    def __init__(self, customers):
        self.customers = customers
        self.next_to_arrive = 0
    
    def more_customer_to_arrive(self):
        return self.next_to_arrive < len(self.customers)

    def process_next_arrival(self):
        if self.more_customer_to_arrive():
            next_arrival = self.customers[self.next_to_arrive]
            self.next_to_arrive += 1
            return next_arrival
        return None 

    def peek_next_arrival(self):
        if self.more_customer_to_arrive():
            next_arrival = self.customers[self.next_to_arrive]
            return next_arrival
        return None 

class Timer:
    def __init__(self):
        self.time = 0
    def update_time(self, new_time):
        self.time = new_time


# Read num tellers from CLI
num_teller = int(input('Enter preferred number of tellers: '))
# Read file name from CLI
file_name = input('Enter input file name: ')
file = open(file_name, 'r')
  
# Read every line from file and for each line create respective customer object and initialize customer manager
customers = []

while True:  
    # Get next line from file
    line = file.readline()
    words = line.split(" ") 
  
    # reach end signal
    if len(words) == 2:
        break

    customers.append(Customer(float(words[0]), float(words[1]), int(words[2])))
    
file.close()
print("Total Number of Customers: {}".format(len(customers)))
customer_manager = CustomerManager(customers)

# Create all the tellers object and initiate the Teller Manager
tellers = []
for num in range(num_teller):
    tellers.append(Teller())
teller_manager = TellerManager(tellers)

# Start the timer
timer = Timer()

# Initialise the priority queue
priority_queue = []

# Max queue length
max_queue_length = 0

def process_service_end(earliest_service_end):
    timer.update_time(earliest_service_end)
    teller_manager.finish_earliest_service()
    if priority_queue:
        highest_priority_customer = max_heap_functions.remove_root(priority_queue)
        teller_manager.serve_customer(highest_priority_customer, timer.time)

def process_arrival():
    global max_queue_length
    if customer_manager.more_customer_to_arrive():
        arrived_customer = customer_manager.process_next_arrival()
        timer.update_time(arrived_customer.arrive_time)
        max_heap_functions.add(priority_queue, arrived_customer)
        max_queue_length = max(max_queue_length, len(priority_queue))

        if teller_manager.free:
            highest_priority_customer = max_heap_functions.remove_root(priority_queue)
            teller_manager.serve_customer(highest_priority_customer, timer.time)

# Program main loop
# This will keep going when there are still customers being served, in the queue or haven't arrived
while teller_manager.busy or priority_queue or customer_manager.more_customer_to_arrive():
    if teller_manager.busy:
        earliest_service_end = teller_manager.earliest_service_end()
        next_arrival = customer_manager.peek_next_arrival()
        
        if not next_arrival or next_arrival.arrive_time > earliest_service_end :
            process_service_end(earliest_service_end)
        else:
            process_arrival()
    else:
        process_arrival()

# Print out the ouput of the program
total_service_time = 0
total_wait_time = 0
for i, customer in enumerate(customers):
    # print("Customer {} with priority {} arrived at {}, served at {}, left at {}".format(i, customer.priority, customer.arrive_time, customer.actual_served_time, customer.leave_time()))
    # print("Wait time: {}".format(customer.wait_time()))
    total_service_time += customer.duration
    total_wait_time += customer.wait_time()
print(f"Every customers are served at {timer.time}")
print("Average service time: {}".format(total_service_time / len(customers)))
print("Average wait time: {}".format(total_wait_time / len(customers)))
print("Max queue length: {}".format(max_queue_length))
print("Average queue length: {}".format(total_wait_time / timer.time))

for i, teller in enumerate(tellers):
    idle_rate = (timer.time - teller.duration_served) / timer.time
    print("Teller {} served {} customers, idle rate: {}".format(i, teller.times_served, idle_rate))