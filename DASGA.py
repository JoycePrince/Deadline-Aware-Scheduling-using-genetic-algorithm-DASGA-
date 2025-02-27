#!/usr/bin/env python
# coding: utf-8

# In[1]:


def get_task_input():
    num_tasks = int(input("Enter the number of tasks: "))
    tasks = [{'name': f'Task {i + 1}', 'units': int(input(f"Enter the task units for Task {i + 1}: ")), 'completion_time': 0.0} for i in range(num_tasks)]
    return tasks

def get_server_input():
    num_servers = int(input("Enter the number of servers: "))
    servers = [{'name': f'Server {i + 1}', 'units': int(input(f"Enter the processing units for Server {i + 1}: ")), 'completion_units': 0, 'tasks': []} for i in range(num_servers)]
    return servers

def schedule_tasks(tasks, servers):
    
    first_task = tasks.pop(0)
    first_server = servers[0]
    first_server['tasks'].append(first_task)
    first_server['completion_units'] += first_task['units']
    first_task['completion_time'] = first_task['units'] / first_server['units']

    for task in sorted(tasks, key=lambda x: x['units'] / x['completion_time'] if x['completion_time'] > 0 else float('inf')):
        free_servers = [server for server in servers if server['completion_units'] == min(server['completion_units'] for server in servers)]
        selected_server = min(free_servers, key=lambda x: x['units'])
        completion_time = task['units'] / selected_server['units']
        task['completion_time'] = completion_time
        selected_server['tasks'].append(task)
        selected_server['completion_units'] += task['units']

    print("\nTask Schedule:")
    max_completion_time = 0
    for server in servers:
        print(f"\n{server['name']}:")
        total_completion_time = sum(task['completion_time'] for task in server['tasks'])
        for task in server['tasks']:
            print(f"  Task {task['name']} assigned, Task Units: {task['units']}, Completion Time: {task['completion_time']}")
        print(f"  Total Completion Time: {total_completion_time} ")
        if total_completion_time > max_completion_time:
            max_completion_time = total_completion_time

    print(f"\nMakeSpan: {max_completion_time}")
    print(f"\nFitness: {max_completion_time}")

    return max_completion_time, [first_task] + tasks  # Including first task in the returned tasks

# Taking input for tasks and servers outside the function
tasks_input = get_task_input()
servers_input = get_server_input()

max_completion_time, tasks_remaining = schedule_tasks(tasks_input, servers_input)

# Calculate and print new generation tasks outside the function
new_generation_tasks = []
makespan_value = max_completion_time

for task in tasks_remaining:
    task['units'] += makespan_value
    # Initialize 'completion_time' for new tasks
    task['completion_time'] = task['units'] / servers_input[0]['units']  # Using the units of the first server
    new_generation_tasks.append({'name': task['name'], 'units': task['units'], 'completion_time': task['completion_time']})

print("\nNew Generation Tasks:")
for task in new_generation_tasks:
    print(f"{task['name']}, Units: {task['units']}")
# Now, perform scheduling for the new generation tasks
new_tasks_input = new_generation_tasks  # Use the generated new tasks as input
# Get server input for new tasks
def schedule_new_tasks(new_tasks_input, servers):
    # Assign each new task to the first available server once
    for task in new_tasks_input:
        assigned = False
        for server in servers:
            if server['completion_units'] + task['units'] <= sum(s['units'] for s in servers):
                server['tasks'].append(task)
                server['completion_units'] += task['units']
                task['completion_time'] = task['units'] / server['units']
                assigned = True
                break

    # Display the schedule for new tasks
    print("\nTask Schedule for New Generation:")
    max_completion_time2 = 0
    for server in servers:
        print(f"\n{server['name']}:")
        total_completion_time = sum(task['completion_time'] for task in server['tasks'])
        for task in server['tasks']:
            print(f"  Task {task['name']} assigned, Task Units: {task['units']}, Completion Time: {task['completion_time']}")
        print(f"  Total Completion Time: {total_completion_time}")
        if total_completion_time > max_completion_time2:
            max_completion_time2 = total_completion_time

    print(f"\nMakeSpan for New Generation: {max_completion_time2}")

    return max_completion_time2  # Including first task in the returned tasks


max_completion_time2 = schedule_new_tasks(new_tasks_input, servers_input)


# In[ ]:




