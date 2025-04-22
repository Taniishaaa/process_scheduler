from collections import deque

class Process:
    def __init__(self, pid, at, bt, io_requests):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.rt = bt
        self.ct = 0
        self.tat = 0
        self.wt = 0
        self.io_requests = io_requests  # [(cpu_time, io_duration)]
        self.current_io_index = 0
        self.cpu_executed = 0  # How much CPU time has been used


def round_robin(processes, tq):
    current_time = 0
    completed = 0
    arrival_idx = 0
    ready_queue = deque()
    io_queue = []  # [(process, io_completion_time)]
    gantt_chart = []

    processes.sort(key=lambda p: p.at)

    while completed < len(processes):
        # Add newly arrived processes
        while arrival_idx < len(processes) and processes[arrival_idx].at <= current_time:
            ready_queue.append(processes[arrival_idx])
            arrival_idx += 1

        # Move I/O completed processes to ready queue
        io_ready = [p for p, t in io_queue if t <= current_time]
        io_queue = [(p, t) for p, t in io_queue if t > current_time]
        ready_queue.extend(io_ready)

        # CPU is idle
        if not ready_queue:
            next_arrival = processes[arrival_idx].at if arrival_idx < len(processes) else float('inf')
            next_io_complete = min([t for _, t in io_queue], default=float('inf'))
            current_time = min(next_arrival, next_io_complete)
            continue

        selected = ready_queue.popleft()
        executed_time = 0
        start_time = current_time

        while executed_time < tq and selected.rt > 0:
            current_time += 1
            executed_time += 1
            selected.rt -= 1
            selected.cpu_executed += 1

            # Check if any new arrivals during this time
            while arrival_idx < len(processes) and processes[arrival_idx].at <= current_time:
                ready_queue.append(processes[arrival_idx])
                arrival_idx += 1

            # Check if any I/O completes during this time
            io_ready = [p for p, t in io_queue if t <= current_time]
            io_queue = [(p, t) for p, t in io_queue if t > current_time]
            ready_queue.extend(io_ready)

            # Check if this process needs I/O now
            if (selected.current_io_index < len(selected.io_requests) and
                selected.cpu_executed == selected.io_requests[selected.current_io_index][0]):
                io_duration = selected.io_requests[selected.current_io_index][1]
                io_complete_time = current_time + io_duration
                io_queue.append((selected, io_complete_time))
                selected.current_io_index += 1
                break  # Stop executing as it goes for I/O

        end_time = current_time
        gantt_chart.append((start_time, end_time, selected.pid))

        if selected.rt == 0:
            selected.ct = current_time
            selected.tat = selected.ct - selected.at
            selected.wt = selected.tat - selected.bt
            completed += 1
        elif selected not in [p for p, _ in io_queue]:  # only requeue if not in I/O
            ready_queue.append(selected)

    result_table = [[p.pid, p.at, p.bt, p.ct, p.tat, p.wt] for p in processes]
    return result_table, gantt_chart
