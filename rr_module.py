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
        self.io_requests = io_requests  # List of (trigger_time, wait_time)
        self.current_io_index = 0


def round_robin(processes, tq):
    completed = 0
    current_time = 0
    arrival_idx = 0
    prev_time = -1

    ready_queue = deque()
    io_queue = deque()

    processes.sort(key=lambda p: p.at)
    gantt_chart = []

    while completed < len(processes):
        while arrival_idx < len(processes) and processes[arrival_idx].at <= current_time:
            ready_queue.append(processes[arrival_idx])
            arrival_idx += 1

        if io_queue and prev_time < current_time:
            for i in range(len(io_queue)):
                io_queue[i][1] -= 1

        while io_queue and io_queue[0][1] <= 0:
            ready_queue.append(io_queue.popleft()[0])

        if not ready_queue:
            prev_time = current_time
            current_time += 1
            continue

        selected = ready_queue.popleft()
        exec_time = min(selected.rt, tq)
        io_triggered = False
        start_time = current_time

        for i in range(exec_time):
            prev_time = current_time
            current_time += 1
            selected.rt -= 1

            while arrival_idx < len(processes) and processes[arrival_idx].at <= current_time:
                ready_queue.append(processes[arrival_idx])
                arrival_idx += 1

            if io_queue:
                for j in range(len(io_queue)):
                    io_queue[j][1] -= 1

            while io_queue and io_queue[0][1] <= 0:
                ready_queue.append(io_queue.popleft()[0])

            for j in range(selected.current_io_index, len(selected.io_requests)):
                selected.io_requests[j][0] -= 1

            if (selected.current_io_index < len(selected.io_requests) and
                selected.io_requests[selected.current_io_index][0] == 0):
                io_queue.append([selected, selected.io_requests[selected.current_io_index][1]])
                selected.current_io_index += 1
                io_triggered = True
                break

        end_time = current_time
        gantt_chart.append((start_time, end_time, selected.pid))  # ✅ Consistent with FCFS

        if selected.rt == 0:
            completed += 1
            selected.ct = current_time
            selected.tat = selected.ct - selected.at
            selected.wt = selected.tat - selected.bt
        elif not io_triggered:
            ready_queue.append(selected)

    result_table = [[p.pid, p.at, p.bt, p.ct, p.tat, p.wt] for p in processes]
    return result_table, gantt_chart  # ✅ Matches FCFS return format