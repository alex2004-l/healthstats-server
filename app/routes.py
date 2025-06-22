import os
import json
from flask import request, jsonify
from app import webserver
from app.task import TaskFactory


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    '''Get result for a job'''
    webserver.logger.info("Got request for job with id %s", job_id)

    # Check if job_id is valid
    id_num = int(job_id)
    if id_num > webserver.job_counter:
        return jsonify({"status": "error", "reason" : "Invalid job_id"})

    if webserver.tasks_runner.get_task_status(id_num) == "done":
        #retrieve the data from the file and return it
        file_path = os.path.join("results", f"job_id_{id_num}.json")
        with open(file_path, "r", encoding='UTF-8') as f:
            result = json.load(f)
        message = {"status": "done", "data" : result}
    else:
        message = {"status": "running"}
    webserver.logger.info("Returned status for job %s", job_id)
    return jsonify(message)


def submit_task_to_threadpool(task_name: str, data, has_state: bool = False):
    '''Helper function for POST methods to submit tasks to the threadpool'''
    webserver.logger.info("Got request : %s", str(data))

    # Not adding tasks in the queue after graceful shutdown
    if not webserver.tasks_runner.get_server_status():
        webserver.logger.info("Request will not be processed because of the shutdown")
        return jsonify({"status": "error", "reason": "shutting down"})

    # Incrementing job_counter
    with webserver.job_lock:
        job_id = webserver.job_counter
        webserver.job_counter += 1

    # Creating task and adding it to queue
    if not has_state:
        new_task = TaskFactory.create_task(
            task_name, job_id, data['question'], webserver.data_ingestor)
    else:
        new_task = TaskFactory.create_task(
            task_name, job_id, data['question'], webserver.data_ingestor, data['state'])

    webserver.tasks_runner.submit_task(new_task)

    message = {"job_id": job_id}
    webserver.logger.info("Returned job id %s", str(message))
    return jsonify(message)


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    '''States_mean request function'''
    data = request.json
    return submit_task_to_threadpool("states_mean", data)
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    '''State_mean request function'''
    data = request.json
    return submit_task_to_threadpool("state_mean", data, True)


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    '''Best5 request function'''
    data = request.json
    return submit_task_to_threadpool("best5", data)


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    '''Worst5 request function'''
    data = request.json
    return submit_task_to_threadpool("worst5", data)


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    '''Global_mean request function'''
    data = request.json
    return submit_task_to_threadpool("global_mean", data)


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    '''Diff_from_mean request function'''
    data = request.json
    return submit_task_to_threadpool("diff_from_mean", data)


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    '''State_diff_from_mean request function'''
    data = request.json
    return submit_task_to_threadpool("state_diff_from_mean", data, True)


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    '''Mean_by_category request function'''
    data = request.json
    return submit_task_to_threadpool("mean_by_category", data)


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    '''State_mean_by_category request function'''
    data = request.json
    return submit_task_to_threadpool("state_mean_by_category", data, True)


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    '''Graceful_shutdown request function'''
    webserver.tasks_runner.graceful_shutdown()
    webserver.logger.info("Got request : %s", str(request.json))

    if webserver.tasks_runner.count_pending_tasks() > 0:
        return jsonify({"status": "running"})
    return jsonify({"status": "done"})


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    '''Jobs request function'''
    webserver.logger.info("Got request : %s", str(request.json))
    message = {"status": "done", "data" : webserver.tasks_runner.get_tasks_status()}
    webserver.logger.info("Returned jobs list : %s", str(message))
    return jsonify(message)


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    '''Num_jobs request function'''
    webserver.logger.info("Got request : %s", str(request.json))
    message = {"num_jobs" : webserver.tasks_runner.count_pending_tasks()}
    webserver.logger.info("Returned number of active jobs : %s", str(message))
    return jsonify(message)


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
