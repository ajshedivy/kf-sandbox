#!/bin/bash

image_name=docker.io/ajshedivy/kf-pipeline-data-quality
image_tag=latest
full_image_name=${image_name}:${image_tag}

# build docker image
docker build -t "${full_image_name}" .

# push docker image
docker push "${full_image_name}"

# output the image digest, which contains immutable information about the built image
docker inspect --format='{{index .RepoDigests 0}}' "${full_image_name}"


