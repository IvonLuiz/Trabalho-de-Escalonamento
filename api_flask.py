from flask import Flask, request, jsonify
from flask_cors import CORS

from system import System

app = Flask(__name__)
CORS(app)
system_instance = System()

#ainda definir quais serão as rotas a serem ouvidas

@app.route('/api/start', methods=['POST'])
def processar_dados():
    try:
        dados_json = request.get_json()

        processes_list = dados_json.get('processesList', [])
        scheduling_algorithm = dados_json.get('schedulingAlgorithm', '')
        paging_algorithm = dados_json.get('pagingAlgorithm', '')
        quantum = dados_json.get('quantum', 0)
        overhead = dados_json.get('overhead', 0)
        delay = dados_json.get('delay', 0)

        system_instance.set_processes_list(processes_list)
        system_instance.set_quantum(quantum)
        system_instance.set_overhead(overhead)
        system_instance.set_delay(delay)

        system_instance.exec_algorithm(scheduling_algorithm, paging_algorithm)

        response = {'status': 'success', 'message': 'Dados recebidos com sucesso.'}

        return jsonify(response), 200
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500


@app.route('/api/reset', methods=['POST'])
def reset_system():
    global system_instance
    system_instance = System()  # Reinicia a instância da classe System
    return jsonify({"status": "success", "message": "System instance reset"})

if __name__ == "__main__":
    app.run(debug=True)
