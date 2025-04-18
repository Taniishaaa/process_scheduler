from flask import Flask, render_template, request
from sjf_module import Process as SJFProcess, sjf_with_io
from fcfs_module import Process as FCFSProcess, fcfs_with_io
from rr_module import Process as RRProcess, round_robin
from srtn_module import Process as SRTNProcess, srtn  
from priority_module import Process as PriorityProcess, priority_scheduling

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landing.html")

# Round Robin
@app.route("/roundrobin", methods=["GET", "POST"])
def roundrobin():
    if request.method == "POST":
        num_processes = int(request.form["num_processes"])
        time_quantum = int(request.form["time_quantum"])
        processes = []

        for i in range(1, num_processes + 1):
            at = int(request.form.get(f"p{i}_at", 0))
            bt = int(request.form.get(f"p{i}_bt", 0))
            io_count = int(request.form.get(f"p{i}_io_count", 0))

            io_requests = []
            for j in range(1, io_count + 1):
                io_trigger = int(request.form.get(f"p{i}_io{j}_trigger", -1))
                io_wait = int(request.form.get(f"p{i}_io{j}_wait", 0))
                io_requests.append([io_trigger, io_wait])

            processes.append(RRProcess(i, at, bt, io_requests))

        # Call the round_robin function to get results and gantt chart data
        results, gantt_chart = round_robin(processes, time_quantum)
        
        # Return the results to the template
        return render_template("index.html", results=results, gantt=gantt_chart)

    return render_template("index.html", results=None, gantt=None)


# FCFS
@app.route("/fcfs", methods=["GET", "POST"])
def fcfs():
    if request.method == "POST":
        num_processes = int(request.form["num_processes"])
        processes = []

        for i in range(num_processes):
            at = int(request.form.get(f"arrival_time_{i}", 0))
            bt = int(request.form.get(f"burst_time_{i}", 0))
            io_count = int(request.form.get(f"io_count_{i}", 0))

            io_requests = []
            for j in range(io_count):
                io_trigger = int(request.form.get(f"io_trigger_{i}_{j}", -1))
                io_wait = int(request.form.get(f"io_wait_{i}_{j}", 0))
                io_requests.append((io_trigger, io_wait))

            processes.append(FCFSProcess(i + 1, at, bt, io_requests))

        results, gantt_chart = fcfs_with_io(processes)  # Updated to return gantt_chart
        return render_template("fcfs.html", results=results, gantt=gantt_chart)

    return render_template("fcfs.html", results=None, gantt=None)


# SJF
@app.route("/sjf", methods=["GET", "POST"])
def sjf():
    if request.method == "POST":
        num_processes = int(request.form["num_processes"])
        processes = []

        for i in range(1, num_processes + 1):
            at = int(request.form.get(f"p{i}_at", 0))
            bt = int(request.form.get(f"p{i}_bt", 0))
            io_count = int(request.form.get(f"p{i}_io_count", 0))

            io_requests = []
            for j in range(1, io_count + 1):
                io_trigger = int(request.form.get(f"p{i}_io{j}_trigger", -1))
                io_wait = int(request.form.get(f"p{i}_io{j}_wait", 0))
                io_requests.append([io_trigger, io_wait])

            processes.append(SJFProcess(i, at, bt, io_requests))

        # Run the SJF algorithm with I/O handling
        results, gantt_chart = sjf_with_io(processes)  # Updated to return gantt_chart
        return render_template("sjf.html", results=results, gantt=gantt_chart)

    return render_template("sjf.html", results=None, gantt=None)

# SRTN
@app.route("/srtn", methods=["GET", "POST"])
def srtn_route():
    if request.method == "POST":
        num_processes = int(request.form["num_processes"])
        processes = []

        for i in range(1, num_processes + 1):
            at = int(request.form.get(f"p{i}_at", 0))
            bt = int(request.form.get(f"p{i}_bt", 0))
            io_count = int(request.form.get(f"p{i}_io_count", 0))

            io_requests = []
            for j in range(1, io_count + 1):
                io_trigger = int(request.form.get(f"p{i}_io{j}_trigger", -1))
                io_wait = int(request.form.get(f"p{i}_io{j}_wait", 0))
                io_requests.append([io_trigger, io_wait])

            processes.append(SRTNProcess(i, at, bt, io_requests))

        results, gantt_chart = srtn(processes)  # Assuming srtn function returns both results and gantt_chart
        return render_template("srtn.html", results=results, gantt=gantt_chart)  # Pass gantt_chart as gantt to the template

    return render_template("srtn.html", results=None, gantt=None)  # Return empty gantt if no results


# Priority Scheduling
@app.route("/priority", methods=["GET", "POST"])
def priority():
    if request.method == "POST":
        num_processes = int(request.form["num_processes"])
        processes = []

        # Collect the data for each process
        for i in range(1, num_processes + 1):
            at = int(request.form.get(f"p{i}_at", 0))
            bt = int(request.form.get(f"p{i}_bt", 0))
            prio = int(request.form.get(f"p{i}_priority", 0))
            io_count = int(request.form.get(f"p{i}_io_count", 0))

            io_requests = []
            for j in range(1, io_count + 1):
                io_trigger = int(request.form.get(f"p{i}_io{j}_trigger", -1))
                io_wait = int(request.form.get(f"p{i}_io{j}_wait", 0))
                io_requests.append([io_trigger, io_wait])

            processes.append(PriorityProcess(i, at, bt, prio, io_requests))

        # Call the priority_scheduling function to get results and Gantt chart data
        results, gantt_chart = priority_scheduling(processes)

        # Pass both results and Gantt chart to the template
        return render_template("priority.html", results=results, gantt=gantt_chart)

    return render_template("priority.html", results=None, gantt=None)



if __name__ == "__main__":
    app.run(debug=True)
