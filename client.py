import json
import socket
import uuid
import re
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from config import COORDINATOR_HOST, COORDINATOR_PORT, SOCKET_TIMEOUT


# =========================================================
# NETWORK COMMUNICATION
# =========================================================

def send_request(request):
    with socket.create_connection(
        (COORDINATOR_HOST, COORDINATOR_PORT),
        timeout=SOCKET_TIMEOUT
    ) as sock:

        sock.sendall(
            (json.dumps(request) + "\n").encode("utf-8")
        )

        data = b""

        while b"\n" not in data:
            chunk = sock.recv(4096)

            if not chunk:
                break

            data += chunk

        if not data:
            raise ConnectionError(
                "Coordinator returned no response."
            )

        return json.loads(
            data.decode("utf-8").strip()
        )


# =========================================================
# DISTRIBUTED CALCULATOR DASHBOARD
# =========================================================

class CalculatorApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "NEXUS | Distributed Calculator"
        )

        self.root.geometry("1150x760")
        self.root.minsize(950, 650)

        # ---------------- COLORS ----------------

        self.bg = "#0b1020"
        self.sidebar_bg = "#0e1729"
        self.panel = "#121a2b"
        self.card = "#19243a"
        self.input_bg = "#222f48"
        self.border = "#2b3954"

        self.white = "#f1f5f9"
        self.muted = "#91a0b8"

        self.blue = "#38bdf8"
        self.green = "#4ade80"
        self.red = "#fb7185"

        self.root.configure(bg=self.bg)

        # ---------------- STATE ----------------

        self.expression = ""
        self.history = []
        self.total_calculations = 0
        self.busy = False

        self.build_ui()

        self.root.bind(
            "<Return>",
            lambda event: self.calculate()
        )

        self.root.bind(
            "<Escape>",
            lambda event: self.clear_all()
        )

        self.root.bind(
            "<Key>",
            self.keyboard_input
        )

        self.refresh_worker_status()

    # =====================================================
    # MAIN UI
    # =====================================================

    def build_ui(self):

        # ---------------- SIDEBAR ----------------

        self.sidebar = tk.Frame(
            self.root,
            bg=self.sidebar_bg,
            width=205
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="◈ NEXUS",
            font=("Segoe UI", 23, "bold"),
            bg=self.sidebar_bg,
            fg=self.blue
        ).pack(
            anchor="w",
            padx=22,
            pady=(28, 2)
        )

        tk.Label(
            self.sidebar,
            text="DISTRIBUTED SYSTEMS",
            font=("Segoe UI", 8, "bold"),
            bg=self.sidebar_bg,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 32)
        )

        self.sidebar_button(
            "▣   Dashboard",
            active=True
        )

        self.sidebar_button(
            "⌘   Calculator"
        )

        self.sidebar_button(
            "◷   History"
        )

        tk.Frame(
            self.sidebar,
            bg=self.border,
            height=1
        ).pack(
            fill="x",
            padx=18,
            pady=24
        )

        tk.Label(
            self.sidebar,
            text="SYSTEM ARCHITECTURE",
            font=("Segoe UI", 8, "bold"),
            bg=self.sidebar_bg,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=20
        )

        tk.Label(
            self.sidebar,
            text=(
                "CLIENT\n"
                "   ↓\n"
                "COORDINATOR\n"
                "   ↓\n"
                "WORKER NODES"
            ),
            font=("Consolas", 10),
            bg=self.sidebar_bg,
            fg=self.blue,
            justify="left"
        ).pack(
            anchor="w",
            padx=22,
            pady=16
        )

        tk.Label(
            self.sidebar,
            text="TCP SOCKETS  •  PYTHON",
            font=("Segoe UI", 8),
            bg=self.sidebar_bg,
            fg=self.muted
        ).pack(
            side="bottom",
            pady=22
        )

        # ---------------- MAIN CONTENT ----------------

        self.main = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True,
            padx=28,
            pady=24
        )

        self.build_header()
        self.build_statistics()
        self.build_workspace()

    # =====================================================
    # SIDEBAR BUTTONS
    # =====================================================

    def sidebar_button(
        self,
        text,
        active=False
    ):

        button = tk.Button(
            self.sidebar,
            text=text,
            font=("Segoe UI", 10, "bold" if active else "normal"),
            bg="#19314a" if active else self.sidebar_bg,
            fg=self.white if active else self.muted,
            activebackground="#19314a",
            activeforeground=self.white,
            anchor="w",
            padx=16,
            pady=13,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

        if text.endswith("History"):
            button.config(
                command=self.focus_history
            )

        elif text.endswith("Calculator"):
            button.config(
                command=self.focus_calculator
            )

        else:
            button.config(
                command=self.focus_calculator
            )

    # =====================================================
    # HEADER
    # =====================================================

    def build_header(self):

        header = tk.Frame(
            self.main,
            bg=self.bg
        )

        header.pack(
            fill="x",
            pady=(0, 22)
        )

        title_frame = tk.Frame(
            header,
            bg=self.bg
        )

        title_frame.pack(
            side="left"
        )

        tk.Label(
            title_frame,
            text="DISTRIBUTED COMPUTING",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg,
            fg=self.blue
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="Control Dashboard",
            font=("Segoe UI", 25, "bold"),
            bg=self.bg,
            fg=self.white
        ).pack(
            anchor="w",
            pady=(2, 2)
        )

        tk.Label(
            title_frame,
            text="Calculate smarter. Distribute workloads.",
            font=("Segoe UI", 10),
            bg=self.bg,
            fg=self.muted
        ).pack(
            anchor="w"
        )

        status_frame = tk.Frame(
            header,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        status_frame.pack(
            side="right",
            pady=8
        )

        self.status_dot = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 11),
            bg=self.panel,
            fg=self.muted
        )

        self.status_dot.pack(
            side="left",
            padx=(12, 5),
            pady=10
        )

        self.status_text = tk.Label(
            status_frame,
            text="CHECKING SYSTEM",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel,
            fg=self.white
        )

        self.status_text.pack(
            side="left",
            padx=(0, 12)
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def build_statistics(self):

        stats = tk.Frame(
            self.main,
            bg=self.bg
        )

        stats.pack(
            fill="x",
            pady=(0, 20)
        )

        self.make_stat_card(
            stats,
            "SUPPORTED OPERATIONS",
            "04",
            "Addition, subtraction, multiplication, division"
        )

        self.make_stat_card(
            stats,
            "WORKER NODES",
            "02",
            "Specialized arithmetic workers"
        )

        self.make_stat_card(
            stats,
            "CALCULATIONS",
            "0",
            "Completed in this session",
            dynamic=True
        )

    def make_stat_card(
        self,
        parent,
        title,
        value,
        description,
        dynamic=False
    ):

        card = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            bg=self.panel,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=13,
            pady=(12, 3)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 22, "bold"),
            bg=self.panel,
            fg=self.blue
        )

        value_label.pack(
            anchor="w",
            padx=13
        )

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 8),
            bg=self.panel,
            fg=self.muted,
            wraplength=220,
            justify="left"
        ).pack(
            anchor="w",
            padx=13,
            pady=(2, 12)
        )

        if dynamic:
            self.total_label = value_label

    # =====================================================
    # WORKSPACE
    # =====================================================

    def build_workspace(self):

        workspace = tk.Frame(
            self.main,
            bg=self.bg
        )

        workspace.pack(
            fill="both",
            expand=True
        )

        # Calculator

        self.calculator_panel = tk.Frame(
            workspace,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.calculator_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # Right panel

        right = tk.Frame(
            workspace,
            bg=self.bg,
            width=280
        )

        right.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        right.pack_propagate(False)

        self.build_calculator()
        self.build_routing(right)
        self.build_history(right)

    # =====================================================
    # CALCULATOR
    # =====================================================

    def build_calculator(self):

        panel = self.calculator_panel

        tk.Label(
            panel,
            text="CALCULATOR",
            font=("Segoe UI", 12, "bold"),
            bg=self.panel,
            fg=self.white
        ).pack(
            anchor="w",
            padx=18,
            pady=(17, 3)
        )

        tk.Label(
            panel,
            text="Enter an expression or use the keypad",
            font=("Segoe UI", 9),
            bg=self.panel,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        display = tk.Frame(
            panel,
            bg=self.input_bg,
            highlightbackground=self.border,
            highlightthickness=1
        )

        display.pack(
            fill="x",
            padx=16,
            pady=(0, 12)
        )

        self.expression_label = tk.Label(
            display,
            text="Ready for calculation",
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.muted,
            anchor="e"
        )

        self.expression_label.pack(
            fill="x",
            padx=12,
            pady=(10, 2)
        )

        self.display_label = tk.Label(
            display,
            text="0",
            font=("Segoe UI", 27, "bold"),
            bg=self.input_bg,
            fg=self.white,
            anchor="e"
        )

        self.display_label.pack(
            fill="x",
            padx=12,
            pady=(0, 10)
        )

        keypad = tk.Frame(
            panel,
            bg=self.panel
        )

        keypad.pack(
            fill="both",
            expand=True,
            padx=13,
            pady=(0, 13)
        )

        keys = [
            ["AC", "⌫", "÷", "×"],
            ["7", "8", "9", "−"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "="],
            ["±", "0", ".", "="]
        ]

        for row_index, row in enumerate(keys):

            keypad.rowconfigure(
                row_index,
                weight=1
            )

            for col_index, key in enumerate(row):

                keypad.columnconfigure(
                    col_index,
                    weight=1
                )

                # The second equals button is intentionally omitted.
                if key == "=" and row_index == 4:
                    continue

                if key in ["÷", "×", "−", "+", "="]:
                    bg = "#174568"
                    fg = self.blue

                elif key in ["AC", "⌫", "±"]:
                    bg = self.card
                    fg = self.muted

                else:
                    bg = "#202d44"
                    fg = self.white

                button = tk.Button(
                    keypad,
                    text=key,
                    font=("Segoe UI", 12, "bold"),
                    bg=bg,
                    fg=fg,
                    activebackground=self.blue,
                    activeforeground="#07111f",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda value=key: self.key_press(value)
                )

                button.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )

    # =====================================================
    # DISTRIBUTED ROUTING
    # =====================================================

    def build_routing(self, parent):

        self.routing_panel = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.routing_panel.pack(
            fill="x",
            pady=(0, 14)
        )

        tk.Label(
            self.routing_panel,
            text="DISTRIBUTED ROUTING",
            font=("Segoe UI", 11, "bold"),
            bg=self.panel,
            fg=self.white
        ).pack(
            anchor="w",
            padx=13,
            pady=(15, 12)
        )

        self.make_node(
            self.routing_panel,
            "CLIENT",
            "GUI / User Input"
        )

        self.make_connector(
            self.routing_panel
        )

        self.make_node(
            self.routing_panel,
            "COORDINATOR",
            "Request Router"
        )

        self.make_connector(
            self.routing_panel
        )

        self.worker1_indicator = self.make_node(
            self.routing_panel,
            "WORKER 1",
            "Addition / Subtraction"
        )

        self.worker2_indicator = self.make_node(
            self.routing_panel,
            "WORKER 2",
            "Multiplication / Division"
        )

    def make_node(
        self,
        parent,
        title,
        subtitle
    ):

        box = tk.Frame(
            parent,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=1
        )

        box.pack(
            fill="x",
            padx=12,
            pady=3
        )

        row = tk.Frame(
            box,
            bg=self.card
        )

        row.pack(
            fill="x",
            padx=9,
            pady=(8, 2)
        )

        dot = tk.Label(
            row,
            text="●",
            font=("Segoe UI", 10),
            bg=self.card,
            fg=self.muted
        )

        dot.pack(
            side="left"
        )

        tk.Label(
            row,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=self.card,
            fg=self.white
        ).pack(
            side="left",
            padx=6
        )

        tk.Label(
            box,
            text=subtitle,
            font=("Segoe UI", 8),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 8)
        )

        return dot

    def make_connector(self, parent):

        tk.Label(
            parent,
            text="       ↓",
            font=("Segoe UI", 12, "bold"),
            bg=self.panel,
            fg=self.blue
        ).pack(
            anchor="w",
            padx=12
        )

    # =====================================================
    # HISTORY
    # =====================================================

    def build_history(self, parent):

        history_panel = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        history_panel.pack(
            fill="both",
            expand=True
        )

        heading = tk.Frame(
            history_panel,
            bg=self.panel
        )

        heading.pack(
            fill="x",
            padx=13,
            pady=(15, 8)
        )

        tk.Label(
            heading,
            text="CALCULATION HISTORY",
            font=("Segoe UI", 10, "bold"),
            bg=self.panel,
            fg=self.white
        ).pack(
            side="left"
        )

        tk.Button(
            heading,
            text="Clear",
            command=self.clear_history,
            font=("Segoe UI", 8),
            bg=self.panel,
            fg=self.muted,
            activebackground=self.panel,
            activeforeground=self.white,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            side="right"
        )

        history_frame = tk.Frame(
            history_panel,
            bg=self.panel
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 10)
        )

        self.history_box = tk.Listbox(
            history_frame,
            bg=self.input_bg,
            fg=self.white,
            selectbackground="#174568",
            selectforeground=self.white,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Consolas", 9)
        )

        self.history_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            history_frame,
            command=self.history_box.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.history_box.config(
            yscrollcommand=scrollbar.set
        )

        self.history_box.bind(
            "<Double-Button-1>",
            self.restore_history
        )

        tk.Label(
            history_panel,
            text="Double-click a calculation to reuse it.",
            font=("Segoe UI", 8),
            bg=self.panel,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=13,
            pady=(0, 12)
        )

        # Last request information

        self.last_request = tk.Label(
            history_panel,
            text="No requests yet",
            font=("Consolas", 9),
            bg=self.card,
            fg=self.muted,
            justify="left",
            anchor="w",
            padx=12,
            pady=10,
            wraplength=240
        )

        self.last_request.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

    # =====================================================
    # WORKER STATUS
    # =====================================================

    def refresh_worker_status(self):

        self.check_node(
            COORDINATOR_HOST,
            COORDINATOR_PORT,
            self.status_dot,
            self.status_text,
            "COORDINATOR"
        )

        # Actual TCP connection checks to worker nodes.
        self.check_node(
            "127.0.0.1",
            5001,
            self.worker1_indicator,
            None,
            "WORKER 1"
        )

        self.check_node(
            "127.0.0.1",
            5002,
            self.worker2_indicator,
            None,
            "WORKER 2"
        )

        self.root.after(
            5000,
            self.refresh_worker_status
        )

    def check_node(
        self,
        host,
        port,
        indicator,
        label,
        name
    ):

        try:

            with socket.create_connection(
                (host, port),
                timeout=1
            ):
                online = True

        except OSError:
            online = False

        color = (
            self.green
            if online
            else self.red
        )

        if indicator is not None:
            indicator.config(fg=color)

        if label is not None:

            label.config(
                text=(
                    f"{name} ONLINE"
                    if online
                    else f"{name} OFFLINE"
                )
            )

            self.status_dot.config(
                fg=color
            )

    # =====================================================
    # INTERACTIVE KEYPAD
    # =====================================================

    def key_press(self, key):

        if self.busy:
            return

        if key == "AC":
            self.clear_all()
            return

        if key == "⌫":

            self.expression = self.expression[:-1]

            self.update_display()
            return

        if key == "±":

            if self.expression.startswith("-"):
                self.expression = self.expression[1:]

            elif self.expression:
                self.expression = "-" + self.expression

            self.update_display()
            return

        if key == "=":

            self.calculate()
            return

        if key in ["+", "−", "×", "÷"]:

            if key in ["+", "−", "×", "÷"]:

                if not self.expression:
                    if key == "−":
                        self.expression = "-"
                        self.update_display()
                    return

                self.expression += {
                    "+": "+",
                    "−": "-",
                    "×": "*",
                    "÷": "/"
                }[key]

                self.update_display()
                return

        if key == ".":

            self.expression += "."

        elif key.isdigit():

            self.expression += key

        self.update_display()

    def keyboard_input(self, event):

        if self.busy:
            return

        if event.char.isdigit():

            self.expression += event.char
            self.update_display()

        elif event.char in "+-*/.":

            self.expression += event.char
            self.update_display()

        elif event.char == "=":

            self.calculate()

    def update_display(self):

        self.display_label.config(
            text=self.expression or "0",
            fg=self.white
        )

        self.expression_label.config(
            text="Enter calculation"
        )

    # =====================================================
    # CALCULATION
    # =====================================================

    def calculate(self):

        if self.busy:
            return

        expr = self.expression.strip()

        if not expr:
            return

        pattern = (
            r"\s*(-?\d+(?:\.\d+)?)\s*"
            r"([+\-*/])\s*"
            r"(-?\d+(?:\.\d+)?)\s*"
        )

        match = re.fullmatch(
            pattern,
            expr
        )

        if not match:

            messagebox.showerror(
                "Invalid Expression",
                "Enter one operation at a time.\n\n"
                "Example: 12 + 5"
            )

            return

        a = float(match.group(1))
        symbol = match.group(2)
        b = float(match.group(3))

        operation_map = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div"
        }

        operation = operation_map[symbol]

        if operation == "div" and b == 0:

            messagebox.showerror(
                "Math Error",
                "Division by zero is not allowed."
            )

            return

        request_id = uuid.uuid4().hex[:8]

        request = {
            "request_id": request_id,
            "operation": operation,
            "a": a,
            "b": b
        }

        worker = (
            "Worker 1"
            if operation in ("add", "sub")
            else "Worker 2"
        )

        self.busy = True

        self.status_text.config(
            text="PROCESSING REQUEST"
        )

        self.status_dot.config(
            fg=self.blue
        )

        self.display_label.config(
            fg=self.blue
        )

        self.root.update_idletasks()

        try:

            response = send_request(request)

            if response.get("status") != "success":

                raise RuntimeError(
                    response.get(
                        "error",
                        "Calculation failed."
                    )
                )

            result = response["result"]

            if (
                isinstance(result, float)
                and result.is_integer()
            ):
                result = int(result)

            self.display_label.config(
                text=str(result),
                fg=self.green
            )

            self.expression_label.config(
                text=f"{a:g} {symbol} {b:g} ="
            )

            self.last_request.config(
                text=(
                    f"REQUEST: {request_id}\n\n"
                    f"OPERATION: {operation.upper()}\n"
                    f"WORKER: {worker}\n\n"
                    f"RESULT: {result}\n"
                    f"STATUS: SUCCESS"
                ),
                fg=self.green
            )

            timestamp = datetime.now().strftime(
                "%H:%M:%S"
            )

            history_item = (
                f"{timestamp}  "
                f"{a:g} {symbol} {b:g} = {result}"
            )

            self.history.append({
                "expression": history_item,
                "request": expr
            })

            self.history_box.insert(
                0,
                history_item
            )

            self.total_calculations += 1

            self.total_label.config(
                text=str(self.total_calculations)
            )

            self.status_text.config(
                text=f"{worker.upper()} COMPLETED"
            )

            self.status_dot.config(
                fg=self.green
            )

            self.expression = str(result)

        except (
            ConnectionError,
            ConnectionRefusedError,
            TimeoutError,
            OSError,
            RuntimeError
        ) as exc:

            self.status_text.config(
                text="REQUEST FAILED"
            )

            self.status_dot.config(
                fg=self.red
            )

            self.display_label.config(
                fg=self.red
            )

            messagebox.showerror(
                "Distributed Calculation Error",
                str(exc)
            )

        finally:

            self.busy = False

    # =====================================================
    # HISTORY AND NAVIGATION
    # =====================================================

    def clear_all(self):

        if self.busy:
            return

        self.expression = ""

        self.display_label.config(
            text="0",
            fg=self.white
        )

        self.expression_label.config(
            text="Ready for calculation"
        )

    def clear_history(self):

        self.history.clear()

        self.history_box.delete(
            0,
            tk.END
        )

        self.total_calculations = 0

        self.total_label.config(
            text="0"
        )

    def restore_history(self, event=None):

        selection = self.history_box.curselection()

        if not selection:
            return

        index = selection[0]

        if index < len(self.history):

            self.expression = self.history[index]["request"]

            self.update_display()

    def focus_history(self):

        self.history_box.focus_set()

    def focus_calculator(self):

        self.root.focus_set()


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CalculatorApp(root)

    root.mainloop()