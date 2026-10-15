import json
import socket
import uuid
from config import COORDINATOR_HOST, COORDINATOR_PORT, WORKERS, SOCKET_TIMEOUT

def send_json(conn, data):
    conn.sendall((json.dumps(data) + "\n").encode("utf-8"))

def receive_json(conn):
    data = b""
    while b"\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            return None
        data += chunk
    return json.loads(data.decode("utf-8").strip())

def contact_worker(worker_address, request):
    host, port = worker_address

    with socket.create_connection((host, port), timeout=SOCKET_TIMEOUT) as sock:
        send_json(sock, request)
        return receive_json(sock)

def handle_client(conn, address):
    with conn:
        try:
            request = receive_json(conn)

            if not request:
                return

            request_id = request.get("request_id") or uuid.uuid4().hex[:8]
            operation = request.get("operation")

            if operation not in WORKERS:
                send_json(conn, {
                    "request_id": request_id,
                    "status": "error",
                    "error": "Unsupported operation."
                })
                return

            request["request_id"] = request_id
            worker = WORKERS[operation]

            print(
                f"[{request_id}] Client {address[0]} requested "
                f"{operation}; routing to {worker[0]}:{worker[1]}"
            )

            try:
                result = contact_worker(worker, request)
            except (ConnectionRefusedError, TimeoutError, OSError) as exc:
                result = {
                    "request_id": request_id,
                    "status": "error",
                    "error": f"Worker unavailable: {exc}"
                }

            send_json(conn, result)

        except Exception as exc:
            try:
                send_json(conn, {
                    "request_id": "unknown",
                    "status": "error",
                    "error": str(exc)
                })
            except Exception:
                pass

def start_server():
    print("=" * 55)
    print("Distributed Calculator - Coordinator")
    print(f"Address : {COORDINATOR_HOST}:{COORDINATOR_PORT}")
    print("Status  : RUNNING")
    print("=" * 55)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((COORDINATOR_HOST, COORDINATOR_PORT))
    server.listen(20)

    try:
        while True:
            conn, address = server.accept()
            import threading
            threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\nCoordinator stopped.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
