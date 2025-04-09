import os
import json
from flask import request, jsonify
from app import webserver
from app.task import TaskFactory


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    if request.method == 'GET':
        print(f"JobID is {job_id}")
        # Check if job_id is valid
        id_num = int(job_id)
        if id_num > webserver.job_counter:
            return jsonify({"status": "error", "reason" : "Invalid job_id"})

        if webserver.tasks_runner.get_task_status(id_num) == "done":
            #retrieve the data from the file and return it
            file_path = os.path.join("results", f"job_id_{id_num}.json")
            with open(file_path, "r") as f:
                result = json.load(f)
            return jsonify({"status": "done", "data" : result})

        return jsonify({"status": "running"})
    else:
        return jsonify({"error": "Method not allowed"}), 405


def add_task_to_threadpool(task_name: str, data, has_state: bool = False):
    with webserver.job_lock:
        job_id = webserver.job_counter
        webserver.job_counter += 1

    if not has_state:
        new_task = TaskFactory.create_task(
            task_name, job_id, data['question'], webserver.data_ingestor)
    else:
        new_task = TaskFactory.create_task(
            task_name, job_id, data['question'], webserver.data_ingestor, data['state'])

    webserver.tasks_runner.submit_task(new_task)

    return jsonify({"job_id": job_id})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("states_mean", data)
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("state_mean", data, True)
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("best5", data)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("worst5", data)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("global_mean", data)
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("diff_from_mean", data)
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("state_diff_from_mean", data, True)
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("mean_by_category", data)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        return add_task_to_threadpool("state_mean_by_category", data, True)
    return jsonify({"error": "Method not allowed"}), 405

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
