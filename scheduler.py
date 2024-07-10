import time
import threading
import socketio

sio = socketio.Client(engineio_logger=True)

def scheduled_function():
    return "Hello, this is the scheduled function output!"

def job():
    while True:
        output = scheduled_function()
        sio.emit('inference', {'data': output}, namespace='/schedule')
        print(output)
        time.sleep(60)  # wait for 1 minute

def start_socket_connection():
    sio.connect('http://127.0.0.1:5000', namespaces=['/schedule'])
    sio.wait()

if __name__ == "__main__":
    sio.connect('http://127.0.0.1:5000', namespaces=['/schedule'])
    job_thread = threading.Thread(target=job, daemon=True)
    job_thread.start()
    sio.wait()
