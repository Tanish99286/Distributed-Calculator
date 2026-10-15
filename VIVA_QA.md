# Viva Questions and Answers

### 1. What is distributed computing?
Distributed computing is a method in which multiple independent computers or processes communicate over a network and work together to complete tasks.

### 2. What is a distributed calculator?
It is a calculator in which calculation requests are distributed to separate worker processes instead of being performed by one program alone.

### 3. Why did you use a coordinator?
The coordinator receives client requests and routes each operation to the correct worker node.

### 4. What is a worker node?
A worker node is an independent process that performs a specific part of the computation.

### 5. What protocol is used?
TCP is used because it provides reliable communication between the client, coordinator, and workers.

### 6. Why is JSON used?
JSON provides a simple and readable format for sending structured data such as operation, numbers, request ID, and result.

### 7. Is the calculator really distributed?
Yes. The client, coordinator, and worker nodes run as separate processes and communicate using TCP sockets. The arithmetic is performed by worker processes rather than the client or coordinator.

### 8. What happens if a worker is not running?
The coordinator catches the connection failure and returns a worker-unavailable error to the client.

### 9. What happens when division by zero is attempted?
The worker checks the second number before performing division and returns an error instead of crashing.

### 10. Can the workers run on different computers?
Yes. The host addresses in config.py can be changed so that the coordinator connects to workers on other computers on the same network.

### 11. What is the role of threading?
The coordinator and workers use threads so they can accept and handle multiple client connections without blocking the whole server.

### 12. What is the main limitation?
The coordinator is a central point for routing. If it stops, clients cannot reach the workers through the normal application flow.

### 13. How can you improve the project?
Load balancing, worker health checks, authentication, encryption, additional operations, and database-based history can be added.

### 14. What is message passing?
Message passing is the exchange of data between independent processes through a communication mechanism such as a network socket.

### 15. What is the difference between a normal calculator and this project?
A normal calculator usually performs calculations inside one program. This project separates the calculation into independent processes that communicate over a network.
