COORDINATOR_HOST = "127.0.0.1"
COORDINATOR_PORT = 6000

WORKERS = {
    "add": ("127.0.0.1", 5001),
    "sub": ("127.0.0.1", 5001),
    "mul": ("127.0.0.1", 5002),
    "div": ("127.0.0.1", 5002),
}

SOCKET_TIMEOUT = 5
