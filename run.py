import os
import signal
import subprocess
import sys
import time


def start_uvicorn():
    os.chdir("app")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def start_fetch_agent():
    os.chdir("..")
    return subprocess.Popen([sys.executable, "sampleAgent/sampleAgent.py"])

def main():
    # Start Uvicorn server
    uvicorn_process = start_uvicorn()
    print("Uvicorn server started.")
    time.sleep(5)

    # Start Fetch.ai agent
    fetch_agent_process = start_fetch_agent()
    print("Fetch.ai agent started.")

    # Handle termination signals to gracefully shut down both processes
    def signal_handler(sig, frame):
        print('Terminating processes...')
        uvicorn_process.terminate()
        fetch_agent_process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Wait for processes to complete
    uvicorn_process.wait()
    fetch_agent_process.wait()

if __name__ == "__main__":
    main()
