class Process:
    def __init__(self, pid, arrival_time, burst_time, io_requests):
        self.pid = pid 
        self.at = arrival_time  
        self.bt = burst_time   
        self.executed_time = 0  
        
        self.io_requests = [[trigger_time, wait_time, False] for trigger_time, wait_time in io_requests]
        self.is_in_io = False
        self.io_completion_time = 0  
        self.is_completed = False  
        self.ct = 0  
        self.tat = 0 
        self.wt = 0  

    def remaining_time(self):
        return self.bt - self.executed_time


def sjf_with_io(processes):
    time = 0
    io_queue = []
    ready_queue = []
    gantt_chart = []  # To store tuples of (start_time, end_time, pid)

    while True:
        # Exit loop if all processes are completed
        if all(p.is_completed for p in processes):
            break

        # Handle I/O completions
        if io_queue:
            io_proc = io_queue[0]
            if time >= io_proc.io_completion_time:
                io_proc.is_in_io = False
                ready_queue.append(io_proc)
                io_queue.pop(0)

        # Add arrived and non-I/O processes to the ready queue (avoid duplication)
        for p in processes:
            if not p.is_completed and p.at <= time and not p.is_in_io and p not in ready_queue and p not in io_queue:
                ready_queue.append(p)

        # If ready queue is not empty, pick process with shortest remaining time
        if ready_queue:
            ready_queue.sort(key=lambda p: p.remaining_time())
            current = ready_queue.pop(0)

            start_time = time
            went_to_io = False

            while current.executed_time < current.bt:
                time += 1
                current.executed_time += 1

                # Check I/O triggers
                for io in current.io_requests:
                    if not io[2] and current.executed_time == io[0]:
                        io[2] = True
                        current.is_in_io = True
                        current.io_completion_time = time + io[1]
                        io_queue.append(current)
                        went_to_io = True
                        break

                if went_to_io:
                    gantt_chart.append((start_time, time, current.pid))  # Add partial execution segment
                    break

            # If process finished all burst time
            if current.executed_time == current.bt:
                current.ct = time
                current.is_completed = True
                gantt_chart.append((start_time, time, current.pid))  # Final segment
        else:
            time += 1  # CPU idle

    # Calculate Turnaround Time (TAT) and Waiting Time (WT)
    for p in processes:
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt

    return [[p.pid, p.at, p.bt, p.ct, p.tat, p.wt] for p in processes], gantt_chart
