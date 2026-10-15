@echo off
title Distributed Calculator

echo Starting Worker 1...
start "Worker 1 - Add/Sub" cmd /k python worker_arithmetic.py --port 5001 --operations add,sub

timeout /t 1 /nobreak >nul

echo Starting Worker 2...
start "Worker 2 - Mul/Div" cmd /k python worker_arithmetic.py --port 5002 --operations mul,div

timeout /t 1 /nobreak >nul

echo Starting Coordinator...
start "Coordinator" cmd /k python coordinator.py

timeout /t 2 /nobreak >nul

echo Starting Client...
start "Calculator Client" cmd /k python client.py
