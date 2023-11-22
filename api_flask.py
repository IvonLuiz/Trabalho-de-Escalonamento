from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from system import System  # Make sure 'System' is available in the same directory
import json
from process import Process

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

system_instance = System()


# Route to initialize the system with received data
@socketio.on('start')
def process_data(data_json):
    processList= []
    data = json.loads(data_json)
    # # Configure the system with received data
    for i in data['process']:
        currentProcess= Process(
            int(i['id']), 
            int(i['execTime']),
            int(i['deadline']),
            int(i['numberOfPages']),
            int(i['arrivalTime']),    
        )
        processList.append(currentProcess)
    system_instance.set_quantum(int(data['quantum']))
    system_instance.set_overhead(int(data['overHead']))
    system_instance.set_delay(int(data['delay']))
    system_instance.set_processes_list(processList)
    
    # Execute the defined algorithms
    system_instance.exec_algorithm(data['cpuAlgorithm'], data['memoryAlgorithm'])
    socketio.emit('initialValues', [
        {'disk': system_instance.memory.disk.storage},
        {'ram': system_instance.memory.ram.storage},
        {'gantt': system_instance.gant_matrix}]
    )
    while True:
        # Execute each CPU cycle in a while loop
        if not system_instance.process_execution():
            break

        while system_instance.update_gantt_chart():
            socketio.emit('updatedValues', [
                {'disk': system_instance.memory.disk.storage},
                {'ram': system_instance.memory.ram.storage},
                {'gantt': system_instance.gant_matrix}]
            )

    reset_system()


# Route to reset the system instance
@socketio.on('reset_system')
def reset_system():
    global system_instance
    system_instance = System()  # Reset the instance of the System class
    # socketio.emit('system_reset', {})
    print('fiz reset')


@socketio.on('connect')
def handle_connect():
    # Send initial data when a WebSocket client connects
    print("conectado")


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
