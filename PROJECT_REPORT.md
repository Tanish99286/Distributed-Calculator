# DISTRIBUTED CALCULATOR
## Mini Project Report

### 1. Introduction

A distributed system is a collection of independent computers or processes that communicate with one another through a network and work together to perform a task. The Distributed Calculator demonstrates this concept using a calculator application.

The project divides the calculator functionality between multiple worker nodes. A client sends a calculation request to a coordinator server. The coordinator identifies the required operation and forwards the request to the appropriate worker node. The worker performs the calculation and sends the result back through the coordinator to the client.

### 2. Problem Statement

A normal calculator performs all calculations in a single program. The purpose of this project is to demonstrate how a simple calculation can be distributed across multiple independent processes that communicate over a network.

### 3. Objectives

- Understand the basic concept of distributed computing.
- Implement communication between independent processes.
- Use TCP sockets for network communication.
- Divide calculator operations among worker nodes.
- Implement a coordinator that routes requests.
- Provide a simple graphical user interface.
- Handle errors such as invalid input and division by zero.

### 4. Technologies Used

- Python
- TCP/IP sockets
- Tkinter
- JSON
- Multithreading
- VS Code or any Python IDE

### 5. System Architecture

The system contains four logical components:

1. Client
2. Coordinator Server
3. Worker Node 1
4. Worker Node 2

The client is responsible for user interaction. The coordinator acts as the request router. Worker Node 1 handles addition and subtraction, while Worker Node 2 handles multiplication and division.

### 6. Working

When the user enters two numbers and selects an operation, the client creates a request containing a request ID, operation, and two numbers.

The request is sent through a TCP socket to the coordinator. The coordinator checks the operation and selects the appropriate worker from its configuration.

The selected worker receives the request, performs the calculation, and returns a JSON response. The coordinator forwards the response to the client. Finally, the client displays the result and stores the calculation in its history.

### 7. Example

Suppose the user enters:

25 × 5

The sequence is:

Client → Coordinator → Worker 2 → Coordinator → Client

Worker 2 performs:

25 × 5 = 125

The client then displays 125.

### 8. Distributed Computing Concepts Demonstrated

- Resource sharing
- Process distribution
- Client-server communication
- Network communication
- Task routing
- Independent worker processes
- Message passing
- Fault handling
- Concurrency

### 9. Advantages

- Clear separation of responsibilities.
- Worker nodes can be run independently.
- New operations can be added later.
- The coordinator does not need to perform calculations itself.
- The architecture demonstrates real message passing.
- Workers can be moved to different computers on the same network.

### 10. Limitations

- The coordinator is a central routing point.
- The project uses a small number of worker nodes.
- Authentication and encryption are not implemented.
- The current configuration is intended for a college demonstration.

### 11. Future Scope

- Add more worker nodes.
- Add scientific calculator operations.
- Add load balancing between multiple workers.
- Add authentication.
- Add encrypted communication.
- Add a database for calculation history.
- Deploy workers on different computers or cloud servers.
- Add automatic worker health monitoring.

### 12. Conclusion

The Distributed Calculator successfully demonstrates how a computational task can be divided among independent processes. The client communicates with a coordinator, and the coordinator distributes the calculation to specialized worker nodes. TCP sockets provide communication between the components. Although the calculation itself is simple, the project demonstrates important distributed computing concepts such as message passing, process independence, task distribution, and client-server architecture.
