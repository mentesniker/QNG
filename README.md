# QNG
Quantum random number generator. Project created for the IEEE Services hackathon.

## Prerequisites to run a test:

- [Install a git client](https://git-scm.com/downloads)
- [Install docker](https://docs.docker.com/get-docker/)

## How to test it:

First, you have to clone this repository and move inside of it. That is:

    git clone https://github.com/mentesniker/QNG.git
    cd QNG

Then, you have to create a docker image from the provided docker file inside of the directory:

    docker build -t qiskitruntime:latest .

Next you have to create a container from the resulting image of the previous step:

    docker run \
      --rm -d --name qr-test-server \
      --volume="$(pwd)"/qiskit_runtime:/qiskit-runtime/qiskit_runtime \
      --volume="$(pwd)"/logs:/qiskit-runtime/logs \
      -p 8000:8000 \
      -e "NUM_WORKERS=4" \
      qiskitruntime:latest \
      bash start-test-server.sh

Once the previous step has finished you can test the program by using:

    curl -X 'POST' \
        'http://127.0.0.1:8000/jobs' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "programId": "random-number-generator",
        "hub": "string",
        "group": "string",
        "project": "string",
        "backend": "string",
        "params": [
            "{\"greeting\":2000}"
        ]
    }'

After that the server will respond with a job id. You can check the status of the job by executing:

    curl -X 'GET' \
    'http://127.0.0.1:8000/jobs/<job_id>' \
    -H 'accept: application/json'

Where <job_id> is the id of the job that we got in the previous step. Finally, when we see that the job status is completed we can see the result of the job by executing:

    curl -X 'GET' \
    'http://127.0.0.1:8000/jobs/<job_id>/results' \
    -H 'accept: application/json'