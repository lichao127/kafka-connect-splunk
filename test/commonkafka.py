"""
Copyright 2018-2019 Splunk, Inc..

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import requests
import sys
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s -' +
                              ' %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

def create_kafka_connector(setup, params):
    '''
    Create kafka connect connector using kafka connect REST API
    '''
    response = requests.post(url=setup["kafka_connect_url"] + "/connectors", data=json.dumps(params),
                      headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    if response.status_code == 201:
        status = get_kafka_connector_status(setup, params)
        while status is not None and status["connector"]["state"] != "RUNNING":
            status = get_kafka_connector_status(setup, params)
        logger.info("Created connector successfully - " + json.dumps(params))
        return True

    return False

def update_kafka_connector(setup, params):
    '''
    Update kafka connect connector using kafka connect REST API
    '''
    response = requests.put(url=setup["kafka_connect_url"] + "/connectors/" + params["name"] + "/config", data=json.dumps(params["config"]),
                      headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    if response.status_code == 200:
        status = get_kafka_connector_status(setup, params)
        while status is not None and status["connector"]["state"] != "RUNNING":
            status = get_kafka_connector_status(setup, params)
        logger.info("Updated connector successfully - " + json.dumps(params))
        return True

    return False

def delete_kafka_connector(setup, params):
    '''
    Delete kafka connect connector using kafka connect REST API
    '''
    response = requests.delete(url=setup["kafka_connect_url"] + "/connectors/" + params["name"],
                        headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    if response.status_code == 204:
        logger.info("Deleted connector successfully - " + json.dumps(params))
        return True

    return False

def get_kafka_connector_tasks(setup, params):
    '''
    Get kafka connect connector tasks using kafka connect REST API
    '''
    status = -1
    while status != 200:
        response = requests.get(url=setup["kafka_connect_url"] + "/connectors/" + params["name"] + "/tasks",
                                headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
        status = response.status_code

    return len(response.json())

def get_kafka_connector_status(setup, params):
    '''
    Get kafka connect connector tasks using kafka connect REST API
    '''
    response = requests.get(url=setup["kafka_connect_url"] + "/connectors/" + params["name"] + "/status",
                      headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    if response.status_code == 200:
        logger.info("Got connector status successfully")
        return response.json()

    return None

def pause_kafka_connector(setup, params):
    '''
    Pause kafka connect connector using kafka connect REST API
    '''
    response = requests.put(url=setup["kafka_connect_url"] + "/connectors/" + params["name"] + "/pause",
                      headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    if response.status_code == 202:
        status = get_kafka_connector_status(setup, params)
        while status is not None and status["connector"]["state"] != "PAUSED":
            status = get_kafka_connector_status(setup, params)
        logger.info("Paused connector successfully")
        return True

    return False

def resume_kafka_connector(setup, params):
    '''
    Resume kafka connect connector using kafka connect REST API
    '''
    response = requests.put(url=setup["kafka_connect_url"] + "/connectors/" + params["name"] + "/resume",
                      headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    if response.status_code == 202:
        status = get_kafka_connector_status(setup, params)
        while status is not None and status["connector"]["state"] != "RUNNING":
            status = get_kafka_connector_status(setup, params)
        logger.info("Resumed connector successfully")
        return True

    return False

def restart_kafka_connector(setup, params):
    '''
    Restart kafka connect connector using kafka connect REST API
    '''
    response = requests.post(url=setup["kafka_connect_url"] + "/connectors/" + params["name"] + "/restart",
                             headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    if response.status_code == 200 or response.status_code == 204:
        status = get_kafka_connector_status(setup, params)
        while status is not None and status["connector"]["state"] != "RUNNING":
            status = get_kafka_connector_status(setup, params)
        logger.info("Restarted connector successfully")
        return True

    return False
