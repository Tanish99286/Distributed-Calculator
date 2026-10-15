# Distributed Calculator

A simple college-level Distributed Computing project built with Python sockets and Tkinter.

## Architecture

```text
                 +----------------------+
                 |   Calculator Client  |
                 |      (Tkinter GUI)   |
                 +----------+-----------+
                            |
                       TCP Socket
                            |
                            v
                 +----------------------+
                 |  Coordinator Server  |
                 |   Request Router     |
                 +----+------------+----+
                      |            |
                TCP   |            |   TCP
                      v            v
              +-----------+   +-----------+
              | Worker 1  |   | Worker 2  |
              | + and -   |   | * and /   |
              +-----------+   +-----------+
```

The coordinator does not perform the arithmetic itself. It forwards the operation to the appropriate worker node.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Separate worker nodes
- TCP socket communication
- Request IDs for tracking
- Operation history in the GUI
- Worker status display
- Error handling
- Graceful handling of division by zero
- Easy local demonstration using three terminal windows

## Requirements

- Python 3.9+
- No external Python packages are required.

## How to Run

Open a terminal in this project folder.

### Terminal 1 — Start Worker 1

```bash
python worker_arithmetic.py --port 5001 --operations add,sub
```

### Terminal 2 — Start Worker 2

```bash
python worker_arithmetic.py --port 5002 --operations mul,div
```

### Terminal 3 — Start Coordinator

```bash
python coordinator.py
```

### Terminal 4 — Start GUI Client

```bash
python client.py
```

Then use the calculator.

## Example

Input:

- Number 1: `25`
- Number 2: `5`
- Operation: `*`

Flow:

1. Client creates a request.
2. Coordinator receives the request.
3. Coordinator sees that `*` belongs to Worker 2.
4. Worker 2 calculates `25 * 5`.
5. Worker 2 sends `125` back.
6. Coordinator sends the result to the client.
7. Client displays `125`.

## Project Files

- `client.py` — Tkinter calculator interface
- `coordinator.py` — central request router
- `worker_arithmetic.py` — reusable worker-node program
- `config.py` — network configuration
- `requirements.txt` — dependency information
- `start_project.bat` — optional Windows launcher
- `PROJECT_REPORT.md` — ready-to-use project report
- `VIVA_QA.md` — viva questions and answers

## Important

This is a local simulation of distributed computing. The client, coordinator, and workers run as separate processes and communicate over TCP sockets. They can also be moved to different computers on the same network by changing the host settings in `config.py`.
