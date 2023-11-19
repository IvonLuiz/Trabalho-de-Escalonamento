from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from system import System  # Make sure 'System' is available in the same directory

app = Flask(__name__)
socketio = SocketIO(app)

system_instance = System()

processes_list_ram = []
processes_list_disk = []
gantt_matrix = []
average_turnaround = 0

# Route to initialize the system with received data
@socketio.on('start')
def process_data():
    try:
        # Get JSON data from the request
        data_json = request.get_json()

        # Extract information from received data
        processes_list = data_json.get('processesList', [])
        scheduling_algorithm = data_json.get('schedulingAlgorithm', '')
        paging_algorithm = data_json.get('pagingAlgorithm', '')
        quantum = data_json.get('quantum', 0)
        overhead = data_json.get('overhead', 0)
        delay = data_json.get('delay', 0)

        # Configure the system with received data
        system_instance.set_processes_list(processes_list)
        system_instance.set_quantum(quantum)
        system_instance.set_overhead(overhead)
        system_instance.set_delay(delay)

        # Execute the defined algorithms
        system_instance.exec_algorithm(scheduling_algorithm, paging_algorithm)

        # Emit success status to the client
        socketio.emit('update', {'status': 'success', 'message': 'Data received successfully.'})

    except Exception as e:
        # Emit error status to the client
        socketio.emit('update', {'status': 'error', 'message': str(e)})


# Route to reset the system instance
@socketio.on('reset_system')
def reset_system():
    global system_instance
    system_instance = System()  # Reset the instance of the System class
    send_update()


def send_update():
    socketio.send({'processes_list_ram': processes_list_ram, 'processes_list_disk': processes_list_disk, 'gantt_matrix': gantt_matrix}, json=True)


@socketio.on('connect')
def handle_connect():
    # Send initial data when a WebSocket client connects
    emit('update', {'processes_list_ram': processes_list_ram, 'processes_list_disk': processes_list_disk, 'gantt_matrix': gantt_matrix})


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)


