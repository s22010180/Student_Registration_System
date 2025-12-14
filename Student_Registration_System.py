import simpy
import random
import statistics
import matplotlib.pyplot as plt

SIMULATION_DURATION = 180 
NUMBER_OF_OFFICERS = 5       
ARRIVAL_RATE = 1               
SERVICE_RATE = 0.2       

wait_times = []
queue_stats_time = []           
queue_stats_length = []         

def student_registration_process(env, officers):
    # Student arrival
    arrival_time = env.now
    
    # Request officer
    with officers.request() as request:
       
        queue_stats_time.append(env.now)
        queue_stats_length.append(len(officers.queue))
        
        yield request
        
        # Calculate waiting time
        waiting_duration = env.now - arrival_time
        wait_times.append(waiting_duration)
        
        # Service time
        avg_service_duration = 1.0 / SERVICE_RATE
        actual_duration = random.expovariate(1.0 / avg_service_duration)
        yield env.timeout(actual_duration)

def student_arrival_generator(env, officers):
    while True:
        # Generate new student
        yield env.timeout(random.expovariate(ARRIVAL_RATE))
        env.process(student_registration_process(env, officers))

# Run Simulation
env = simpy.Environment()
officers = simpy.Resource(env, capacity=NUMBER_OF_OFFICERS)

env.process(student_arrival_generator(env, officers))
env.run(until=SIMULATION_DURATION)

# Results
if wait_times:
    total_students = len(wait_times)
    avg_wait = statistics.mean(wait_times)
    
    # Average queue size
    if queue_stats_length:
        avg_queue_len = statistics.mean(queue_stats_length)
    else:
        avg_queue_len = 0

    # Calculate utilization
    total_capacity = NUMBER_OF_OFFICERS * SIMULATION_DURATION
    total_busy_time = sum([1.0/SERVICE_RATE for _ in range(total_students)]) 
    utilization = (total_busy_time / total_capacity) * 100

    print("\n ***** Final Results ***** ")
    print("")
    print(f"Total Students Served: {total_students}")
    print(f"Average Wait Time:     {avg_wait:.2f} minutes")
    print(f"Average Queue Length:  {avg_queue_len:.2f} students")
    print(f"Officer Utilization:   {utilization:.2f}%")
    print("")
else:
    print("No students arrived.")

# Graph
plt.figure(figsize=(10, 6))
plt.step(queue_stats_time, queue_stats_length, where='post')
plt.title("Queue Length Over Time")
plt.xlabel("Time (Minutes)")
plt.ylabel("Number of Students Waiting")
plt.grid(True)
plt.show()
