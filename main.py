# Array implementation of a heap
# Function in here will directly modify the order of elemnents
# in the heap
class Max_Heap:
    # Convert a normal array into an array-based heap
    def heapify(arr):
        Len = len(arr)
        for i in range(Len // 2 - 1, -1, -1):
            sift_down(arr, Len, i)

    def sift_up(arr, idx):
        while idx > 0:
            fa = (idx - 1) // 2
            if arr[fa] < arr[idx]:
                arr[fa], arr[idx] = arr[idx], arr[fa]
                idx = fa
            else:
                break

    def sift_down(arr, i):
        Len = len(arr)
        greatest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < Len and arr[greatest] < arr[left]:
            greatest = left

        if right < Len and arr[greatest] < arr[right]:
            greatest = right

        if greatest != i:
            arr[i], arr[greatest] = arr[greatest], arr[i]
            sift_down(arr, greatest)

    def Append(arr, ele):
        arr += [ele]
        return arr

    def insert(arr, newNum):
        Len = len(arr)
        if Len == 0:
            arr = Append(arr, newNum)
        else:
            arr = Append(arr, newNum)
            sift_up(arr, len(arr)-1)

    def Pop(arr):
        if len(arr) > 0:
            return arr[:-1]
        else:
            return

    def deleteNode(arr, num):
        Len = len(arr)
        i = 0
        for i in range(0, Len):
            if num == arr[i]:
                break

        arr[i], arr[Len - 1] = arr[Len - 1], arr[i]
        arr = Pop(arr)
        sift_down(arr, i)


"""
    def siftup(heap, idx):
        while idx > 0:
            fa = (idx - 1) // 2
            if heap[fa] < heap[idx]:
                heap[fa], heap[idx] = heap[idx], heap[fa]
                idx = fa
            else: break

    def siftdown(heap, idx):
        larger_child = idx * 2
        # if this element doesn't have children then stop
        if larger_child >= len(heap): return
        # choose the larger child to compare
        if larger_child + 1 < len(heap) and heap[larger_child] < heap[larger_child + 1]:
            larger_child += 1
        # if child > parent, swap them
        if heap[idx] < heap[larger_child]:
            heap[larger_child], heap[idx] = heap[idx], heap[larger_child]
            Max_Heap.siftdown(heap, larger_child)
"""

"""
    # Add an element to the heap and maintain the heap property
    def add(heap, ele):
        heap.append(ele)
        max_heap_functions.siftup(heap, len(heap) - 1)
"""
"""
    # Remove the root of the heap and maintain the heap property
    @staticmethod
    def remove_root(heap):
        last = len(heap) - 1
        # Swap the root and the last element
        heap[0], heap[last] = heap[last], heap[0]
        root = heap.pop() # remove the last element (which is the root)
        max_heap_functions.siftdown(heap, 0)
        return root
"""


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
        Max_Heap.add(self.busy, teller)

    def finish_earliest_service(self):
        teller = Max_Heap.remove_root(self.busy)
        teller.finish_serving()
        self.free.append(teller)

    def earliest_service_end(self):
        if self.busy:
            return self.busy[0].customer.leave_time()
        else:
            return None


class Customer:
    def __init__(self, a_time, s_time, pk):
        self.a_time = a_time
        self.s_time = s_time
        self.pk = pk
        self.real_time = None

    def wait_time(self):
        return self.real_time - self.a_time

    def finish_served(self):
        return self.real_time + self.s_time

    def __eq__(self, other):
        return self is other

    def __lt__(self, other):
        return (self.pk < other.pk) or (self.a_time > other.a_time)

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __str__(self):
        return f"Customer({self.a_time}, {self.s_time}, {self.pk})"


class ControlCustomer:
    def __init__(self, customers):
        self.customers = customers
        self.next_customer_index = 0

    def has_more_customers(self):
        if self.next_customer_index < len(self.customers):
            return True
        return False

    def get_next_customer(self):
        if self.has_more_customers() == True:
            next_customer = self.customers[self.next_customer_index]
            self.next_customer_index += 1
            return next_customer
        return None

    def peek_next_customer(self):
        if self.has_more_customers() == True:
            return self.customers[self.next_customer_index]
        return None


"""
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
"""


class Timer:
    # Create initial time equal to 0
    def __init__(self):
        self.time = 0
    # Update the time of Customer

    def update_time(self, new_time):
        self.time = new_time
    # Get the current time of Customer

    def get_time(self):
        return self.time


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
customer_manager = ControlCustomer(customers)

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
        highest_priority_customer = Max_Heap.deleteNode(priority_queue)
        teller_manager.serve_customer(highest_priority_customer, timer.time)


def process_arrival():
    global max_queue_length
    if customer_manager.has_more_customers():
        arrived_customer = customer_manager.get_next_customer()
        timer.update_time(arrived_customer.arrive_time)
        Max_Heap.insert(priority_queue, arrived_customer)
        max_queue_length = max(max_queue_length, len(priority_queue))

        if teller_manager.free:
            highest_priority_customer = Max_Heap.deleteNode(priority_queue)
            teller_manager.serve_customer(
                highest_priority_customer, timer.time)


# Program main loop
# This will keep going when there are still customers being served, in the queue or haven't arrived
while teller_manager.busy or priority_queue or customer_manager.has_more_customers():
    if teller_manager.busy:
        earliest_service_end = teller_manager.earliest_service_end()
        next_arrival = customer_manager.peek_next_customer()

        if not next_arrival or next_arrival.arrive_time > earliest_service_end:
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
    print("Teller {} served {} customers, idle rate: {}".format(
        i, teller.times_served, idle_rate))
