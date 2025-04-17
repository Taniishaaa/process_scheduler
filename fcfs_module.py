import heapq
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
        self.io_requests = io_requests  # List of (trigger_time, duration) tuples
        self.current_io_index = 0
        self.waiting_time = 0
        self.io_completion_time = 0
        self.state = "ready"
        self.last_ready_time = 0  #Time it last entered ready state

    def __lt__(self, other):
        #For heapq: prioritize by io_completion_time, then arrival time
        if self.io_completion_time != other.io_completion_time:
            return self.io_completion_time < other.io_completion_time
        return self.at < other.at


def fcfs_with_io(processes):
    completed = 0
    current_time = 0
    ready_queue = deque()
    event_queue = []
    heapq.heapify(event_queue)
    gantt_chart = []  

    for p in processes:
        heapq.heappush(event_queue, (p.at, p, "arrival"))
        p.last_ready_time = p.at

    while completed < len(processes) or ready_queue or event_queue:
        if not ready_queue and event_queue and current_time < event_queue[0][0]:
            current_time = event_queue[0][0]

        while event_queue and event_queue[0][0] <= current_time:
            event_time, process, event_type = heapq.heappop(event_queue)
            current_time = max(current_time, event_time)

            if event_type == "arrival":
                process.state = "ready"
                process.last_ready_time = current_time
                ready_queue.append(process)

            elif event_type == "io_completion":
                process.state = "ready"
                process.last_ready_time = current_time
                ready_queue.append(process)

        if ready_queue:
            current_process = ready_queue.popleft()
            current_process.state = "running"

            time_run = 0
            io_done = False

            if current_process.current_io_index < len(current_process.io_requests):
                trigger_time, io_duration = current_process.io_requests[current_process.current_io_index]
                if current_process.bt - current_process.rt >= trigger_time:
                    current_process.current_io_index += 1
                else:
                    time_until_io = trigger_time - (current_process.bt - current_process.rt)
                    time_run = min(current_process.rt, time_until_io)
                    io_done = True
            else:
                time_run = current_process.rt

            current_process.waiting_time += current_time - current_process.last_ready_time

            start_time = current_time
            current_time += time_run
            end_time = current_time
            gantt_chart.append((start_time, end_time, current_process.pid))  # ✅ Add entry to Gantt

            current_process.rt -= time_run

            if io_done and current_process.rt > 0:
                _, io_duration = current_process.io_requests[current_process.current_io_index]
                current_process.current_io_index += 1
                current_process.io_completion_time = current_time + io_duration
                heapq.heappush(event_queue, (current_process.io_completion_time, current_process, "io_completion"))
                current_process.state = "waiting"
            elif current_process.rt == 0:
                current_process.ct = current_time
                current_process.tat = current_process.ct - current_process.at
                current_process.wt = current_process.tat - current_process.bt
                completed += 1
            else:
                current_process.last_ready_time = current_time
                ready_queue.append(current_process)

    result_table = [[p.pid, p.at, p.bt, p.ct, p.tat, p.wt] for p in processes]
    return result_table, gantt_chart
