import argparse
import json
import socket
import threading

OPERATIONS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
}

def send_json(conn, data):
    message = json.dumps(data) + "\n"
    conn.sendall(message.encode("utf-8"))

def handle_client(conn, address, allowed_operations):
    with conn:
        try:
            data = b""
            while b"\n" not in data:
                chunk = conn.recv(4096)
                if not chunk:
                    return
                data += chunk

            request = json.loads(data.decode("utf-8").strip())

            request_id = request.get("request_id", "unknown")
            operation = request.get("operation")
            a = request.get("a")
            b = request.get("b")

            if operation not in allowed_operations:
                send_json(conn, {
                    "request_id": request_id,
                    "status": "error",
                    "error": "This worker does not handle that operation."
                })
                return

            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                send_json(conn, {
                    "request_id": request_id,
                    "status": "error",
                    "error": "Invalid numeric input."
                })
                return

            if operation == "div" and b == 0:
                send_json(conn, {
                    "request_id": request_id,
                    "status": "error",
                    "error": "Division by zero is not allowed."
                })
                return

            result = OPERATIONS[operation](a, b)

            send_json(conn, {
                "request_id": request_id,
                "status": "success",
                "result": result
            })

            print(f"[{request_id}] {a} {operation} {b} = {result}")

        except (json.JSONDecodeError, ValueError) as exc:
            send_json(conn, {
                "request_id": "unknown",
                "status": "error",
                "error": f"Invalid request: {exc}"
            })
        except Exception as exc:
            try:
                send_json(conn, {
                    "request_id": "unknown",
                    "status": "error",
                    "error": str(exc)
                })
            except Exception:
                pass

def start_server(host, port, operations):
    print("=" * 55)
    print("Distributed Calculator - Worker Node")
    print(f"Address     : {host}:{port}")
    print(f"Operations  : {', '.join(operations)}")
    print("Status      : RUNNING")
    print("=" * 55)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(10)

    try:
        while True:
            conn, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(conn, address, operations),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\nWorker stopped.")
    finally:
        server.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arithmetic worker node")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument(
        "--operations",
        required=True,
        help="Comma-separated operations: add,sub,mul,div"
    )
    args = parser.parse_args()

    operations = [
        item.strip().lower()
        for item in args.operations.split(",")
        if item.strip()
    ]

    invalid = [op for op in operations if op not in OPERATIONS]
    if invalid:
        raise SystemExit(f"Invalid operations: {', '.join(invalid)}")

    start_server(args.host, args.port, operations)
