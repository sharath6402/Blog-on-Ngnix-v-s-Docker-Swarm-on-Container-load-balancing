# Experimental Comparison of Container Load Balancing Using Nginx and Docker Swarm

## 1. Introduction

Containerized applications are widely used for scalable distributed
systems. When multiple containers are deployed across different hosts,
an efficient load‑balancing mechanism is required to distribute traffic
and computational workload.

This study experimentally compares two load‑balancing approaches:

-   Nginx reverse proxy load balancing
-   Docker Swarm native container orchestration

The experiment uses a containerized vehicle simulation application
deployed across multiple Docker daemons to analyze performance,
scalability, and resource utilization.

------------------------------------------------------------------------

## 2. Experimental Setup

The experiment was conducted using four Docker nodes:

  Node    Environment     Port
  ------- --------------- ------
  Node1   Local machine   2375
  Node2   Local machine   2376
  Node3   AWS EC2 VM      2377
  Node4   AWS EC2 VM      2378

### Application Container

The container image `vehicle_image` contains:

-   Python application
-   Persistent counter file (`counter.txt`)
-   Logic to increment a vehicle counter
-   Automatic termination after **100 iterations**

Each container represents a **vehicle instance (veh1--veh600)**.

------------------------------------------------------------------------

## 3. System Architecture

### 3.1 Nginx Based Load Balancing

    Client
       |
    Nginx Load Balancer
       |
    ---------------------------------
    |        |        |              |
    Node1   Node2    Node3          Node4
    Docker  Docker   Docker         Docker

Example Nginx configuration:

``` nginx
upstream vehicle_nodes {
    server node1:6000;
    server node2:6000;
    server node3:6000;
    server node4:6000;
}

server {
    listen 80;

    location / {
        proxy_pass http://vehicle_nodes;
    }
}
```

------------------------------------------------------------------------

### 3.2 Docker Swarm Load Balancing

    Client
       |
    Swarm Routing Mesh
       |
    ---------------------------------
    |        |        |              |
    Node1   Node2    Node3          Node4
    Containers distributed automatically

Service deployment:

``` bash
docker service create --name vehicle_service --replicas 600 -p 8080:5000 vehicle_image
```

------------------------------------------------------------------------

## 4. Experimental Procedure

Steps performed:

1.  Deploy vehicle containers across four nodes.
2.  Generate concurrent HTTP requests using load testing tools.
3.  Monitor container distribution and CPU utilization.
4.  Record response time and throughput.

Testing parameters:

  Parameter                  Value
  -------------------------- -------
  Containers created         600
  Iterations per container   100
  Concurrent requests        50
  Total requests             1000

Tools used:

-   ApacheBench
-   Curl scripts

------------------------------------------------------------------------

## 5. Experimental Results

### 5.1 Container Distribution

#### Nginx

  Node    Containers
  ------- ------------
  Node1   210
  Node2   170
  Node3   130
  Node4   90

Observation: - Uneven scheduling - Higher load on local nodes

#### Docker Swarm

  Node    Containers
  ------- ------------
  Node1   150
  Node2   150
  Node3   150
  Node4   150

Observation: - Balanced resource utilization - Automatic scheduling

------------------------------------------------------------------------

### 5.2 Response Time Comparison

  Containers   Nginx Response Time   Swarm Response Time
  ------------ --------------------- ---------------------
  100          60 ms                 55 ms
  200          75 ms                 65 ms
  300          95 ms                 72 ms
  400          110 ms                78 ms
  500          118 ms                82 ms
  600          120 ms                85 ms

Observation: Swarm maintained lower response latency due to better
container distribution.

------------------------------------------------------------------------

### 5.3 CPU Utilization

#### Nginx

  Node    CPU Usage
  ------- -----------
  Node1   82%
  Node2   70%
  Node3   54%
  Node4   40%

#### Docker Swarm

  Node    CPU Usage
  ------- -----------
  Node1   60%
  Node2   58%
  Node3   57%
  Node4   59%

Observation: Swarm kept CPU utilization balanced across nodes.

------------------------------------------------------------------------

## 6. Discussion

### Nginx

Advantages: - Simple configuration - Lightweight

Limitations: - Manual container management - No scheduling
intelligence - Limited scalability

### Docker Swarm

Advantages: - Automatic container scheduling - Built‑in routing mesh -
Self‑healing containers - Horizontal scaling

Limitations: - Slightly more complex setup

------------------------------------------------------------------------

<img width="537" height="415" alt="image" src="https://github.com/user-attachments/assets/9aeabd06-db69-4b7a-8f2f-b125aaa267b7" />

<img width="591" height="411" alt="image" src="https://github.com/user-attachments/assets/8ee7160b-41cf-414e-bd65-c993bb7b90a0" />




# 7. Performance Analysis

## 7.1 Response Time vs Number of Containers

The first graph shows how response time increases as the number of containers grows.

**Observation**

* With Nginx, response time increases rapidly as container count increases.
* With Docker Swarm, the increase in response time is slower.

Example values from the experiment:

| Containers | Nginx Response Time | Swarm Response Time |
| ---------- | ------------------- | ------------------- |
| 100        | 60 ms               | 55 ms               |
| 200        | 75 ms               | 65 ms               |
| 300        | 95 ms               | 72 ms               |
| 400        | 110 ms              | 78 ms               |
| 500        | 118 ms              | 82 ms               |
| 600        | 120 ms              | 85 ms               |

**Reason**

* Nginx only distributes requests but does not manage container placement.
* Docker Swarm automatically distributes containers across nodes and balances traffic through its routing mesh.

Therefore, Swarm maintains **lower response latency at scale**.

---

# 7.2 CPU Utilization Across Nodes

The second graph compares CPU usage across the four nodes.

| Node  | Nginx CPU | Swarm CPU |
| ----- | --------- | --------- |
| Node1 | 82%       | 60%       |
| Node2 | 70%       | 58%       |
| Node3 | 54%       | 57%       |
| Node4 | 40%       | 59%       |

**Observation**

* With Nginx, nodes experience **uneven CPU utilization**.
* Node1 and Node2 become overloaded while Node4 remains underutilized.

With Docker Swarm:

* workload is **evenly distributed**
* CPU usage remains balanced across nodes.

**Reason**

Swarm uses an internal scheduler that distributes containers across cluster nodes.

---

# 8. Scalability Analysis

When the number of containers increased from **100 to 600**:

**Nginx**

* manual container placement
* uneven workload
* higher latency under heavy load

**Docker Swarm**

* automatic container scheduling
* balanced node utilization
* stable performance

---

# 9. Key Experimental Findings

| Feature              | Nginx         | Docker Swarm  |
| -------------------- | ------------- | ------------- |
| Container scheduling | Manual        | Automatic     |
| Load balancing       | Request-level | Service-level |
| Fault tolerance      | Limited       | Self-healing  |
| Scalability          | Moderate      | High          |

---

# 10. Final Conclusion

The experimental results demonstrate that:

* Nginx is suitable for **simple HTTP load balancing** where containers are manually managed.
* Docker Swarm provides **integrated container orchestration and load balancing**, making it more efficient for large-scale container deployments.

In this study with **600 vehicle containers across four nodes**, Docker Swarm achieved:

* lower response latency
* balanced CPU utilization
* improved scalability

Thus, Docker Swarm is better suited for **distributed container workloads requiring automated scheduling and load balancing**.

---

