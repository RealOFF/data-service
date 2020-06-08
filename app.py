import os
from flask import Flask, request, jsonify
from rq import Queue
from worker import conn

from src.index import start, clean

app = Flask(__name__)
q = Queue(connection=conn)

def get_status(job):
    status = {
        'id': job.id,
        'result': job.result,
        'status': 'failed' if job.is_failed else 'pending' if job.result == None else 'completed'
    }
    status.update(job.meta)
    return status

@app.route("/start")
def handle_fetch_job():
    days = request.args.get('days')
    hours = request.args.get('hours')
    query_id = request.args.get('job')
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            output = get_status(found_job)
        else:
            output = { 'id': None, 'error_message': 'No job exists with the id number ' + query_id }
    else:
        new_job = q.enqueue(start,  args=(days, hours), job_timeout=1000)
        output = get_status(new_job)
    return jsonify(output)

@app.route("/clean")
def handle_clean_job():
    days = request.args.get('days')
    hours = request.args.get('hours')
    query_id = request.args.get('job')
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            output = get_status(found_job)
        else:
            output = { 'id': None, 'error_message': 'No job exists with the id number ' + query_id }
    else:
        new_job = q.enqueue(clean, days, hours)
        output = get_status(new_job)
    return jsonify(output)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)