from collections import deque

class Process:
    def __init__(self, pid, at, bt, priority, io_requests):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.priority = priority
        self.rt = bt
        self.ct = 0
        self.tat = 0
        self.wt = 0
        self.io_requests = io_requests  # List of [trigger_time, wait_time]
        self.current_io_index = 0
        self.executed_time = 0  # Total time executed

def priority_scheduling(processes):
    completed = 0
    current_time = 0
    arrival_idx = 0
    ready_queue = []
    io_queue = deque()
    active_io_process = None
    active_io_time = 0
    gantt_chart = []

    processes.sort(key=lambda p: p.at)

    while completed < len(processes):
        while arrival_idx < len(processes) and processes[arrival_idx].at <= current_time:
            ready_queue.append(processes[arrival_idx])
            arrival_idx += 1

        if active_io_process:
            active_io_time -= 1
            if active_io_time == 0:
                ready_queue.append(active_io_process)
                active_io_process = None

        if not active_io_process and io_queue:
            active_io_process, active_io_time = io_queue.popleft()

        ready_queue.sort(key=lambda p: (p.priority, p.at))

        if not ready_queue:
            current_time += 1
            continue

        selected = ready_queue.pop(0)
        start_time = current_time
        selected.rt -= 1
        selected.executed_time += 1
        current_time += 1
        gantt_chart.append((start_time, current_time, selected.pid))

        if (selected.current_io_index < len(selected.io_requests) and
            selected.executed_time == selected.io_requests[selected.current_io_index][0]):
            io_duration = selected.io_requests[selected.current_io_index][1]
            io_queue.append([selected, io_duration])
            selected.current_io_index += 1
        elif selected.rt > 0:
            ready_queue.append(selected)
        else:
            selected.ct = current_time
            selected.tat = selected.ct - selected.at
            selected.wt = selected.tat - selected.bt
            completed += 1

    return [[p.pid, p.at, p.bt, p.priority, p.ct, p.tat, p.wt] for p in processes], gantt_chart
