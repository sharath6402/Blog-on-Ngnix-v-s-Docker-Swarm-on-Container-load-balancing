from flask import Flask
import docker

app = Flask(__name__)

daemons = [
    "tcp://127.0.0.1:2375",
    "tcp://127.0.0.1:2376",
    "tcp://13.63.154.72:2377",
    "tcp://13.63.154.72:2378"
]

clients = [docker.DockerClient(base_url=d) for d in daemons]

counter = 1


def least_loaded():
    loads = []
    for c in clients:
        loads.append(len(c.containers.list()))
    return loads.index(min(loads))


@app.route("/create")
def create_container():
    global counter

    node = least_loaded()
    client = clients[node]

    IMAGE = "sharu6402/sharath_project:version1"
    CONTAINER = f"veh{counter}"
    VEHICLE_ID = f"veh{counter}.txt"

    client.containers.run(
        IMAGE,
        name=CONTAINER,
        detach=True,
        environment={"VEHICLE_ID": VEHICLE_ID},
        volumes={"vehicle_data": {"bind": "/data", "mode": "rw"}},
        network_mode="none"
    )

    counter += 1

    return f"Container {CONTAINER} created on node {node}"

@app.route("/delete/<int:num>")
def delete_container(num):

    container_name = f"veh{num}"

    for i, client in enumerate(clients):
        try:
            container = client.containers.get(container_name)
            container.remove(force=True)
            return f"{container_name} removed from node {i}"
        except docker.errors.NotFound:
            continue
        except Exception as e:
            return f"Error deleting {container_name}: {str(e)}"

    return f"{container_name} not found on any node"
    
    
app.run(host="0.0.0.0", port=6000, debug=True)
