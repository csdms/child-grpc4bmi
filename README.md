[![Basic Model Interface](https://img.shields.io/badge/CSDMS-Basic%20Model%20Interface-green.svg)](https://bmi.readthedocs.io/)
[![Test](https://github.com/csdms/child-grpc4bmi/actions/workflows/test.yml/badge.svg)](https://github.com/csdms/child-grpc4bmi/actions/workflows/test.yml)
[![Docker Hub](https://github.com/csdms/child-grpc4bmi/actions/workflows/release.yml/badge.svg)](https://github.com/csdms/child-grpc4bmi/actions/workflows/release.yml)
![Docker Image Version](https://img.shields.io/docker/v/csdms/child-grpc4bmi)

# child-grpc4bmi

Set up a [grpc4bmi](https://grpc4bmi.readthedocs.io) server
to run a containerized version of the
[Channel-Hillslope Integrated Landscape Development](https://csdms.colorado.edu/wiki/Model:CHILD) (CHILD) model
through Python.

## Build

Build this example locally with:
```
docker build --tag child-grpc4bmi .
```
The image is built on the [csdms/grpc4bmi](https://hub.docker.com/r/csdms/grpc4bmi) base image,
which is built on the [condaforge/miniforge3](https://hub.docker.com/r/condaforge/miniforge3) base image.
The OS is Linux/Ubuntu.
The CHILD model, grpc4bmi, and the grpc4bmi server are installed in `/opt/conda`.
The CHILD grpc4bmi server is exposed through port 55555.

## Run

Use the grpc4bmi Docker client to access the BMI methods of the containerized model.

Install with *pip*:
```
pip install grpc4bmi
```
Then, in a Python session, access CHILD in the image built above with:
```python
from grpc4bmi.bmi_client_docker import BmiClientDocker


m = BmiClientDocker(image="child-grpc4bmi", image_port=55555, work_dir=".")
m.get_component_name()

del m  # stop container cleanly
```

If the image isn't found locally, it's pulled from Docker Hub
(e.g., try the `csdms/child-grpc4bmi` image).

For more in-depth examples of running the CHILD model through grpc4bmi,
see the [examples](./examples) directory.

## Developer notes

A versioned, multiplatform image is hosted on Docker Hub
at [csdms/child-grpc4bmi](https://hub.docker.com/r/csdms/child-grpc4bmi).
This image is automatically built and pushed to Docker Hub
with the [release](./.github/workflows/release.yml) CI workflow.
The workflow is only run when the repository is tagged.
To manually build and push an update, run:
```
docker buildx build --platform linux/amd64,linux/arm64 -t csdms/child-grpc4bmi:latest --push .
```
A user can pull this image from Docker Hub with:
```
docker pull csdms/child-grpc4bmi
```
optionally with the `latest` tag or with a version tag.

## Acknowledgment

This work is supported by the U.S. National Science Foundation under Award No. [2103878](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2103878), *Frameworks: Collaborative Research: Integrative Cyberinfrastructure for Next-Generation Modeling Science*.
