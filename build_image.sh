#!/bin/bash
if (($# == 0)); then
    echo "usage: bash build_image.sh -n <image_name> -d <directory_name> -t <tag>"
    exit 0
fi

POSITIONAL_ARGS=()
HELP_MSG=NO
POWER=NO

TAG=latest

while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--name)
      NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -d|--dirname)
      DIRNAME="$2"
      shift # past argument
      shift # past value
      ;;
    -t|--tag)
      TAG="$2"
      shift # past argument
      shift # past value
      ;;
    --power)
      POWER=YES
      shift # past argument with no value
      ;;
    --help)
      HELP_MSG=YES
      shift # past argument with no value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done
set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

echo "NAME                  = ${NAME}"
echo "DIRNAME               = ${DIRNAME}"
echo "TAG                   = ${TAG}"
echo "POWER                 = ${POWER}"

cd ${DIRNAME}

image_name=docker.io/ajshedivy/${NAME}
image_tag=${TAG}
full_image_name=${image_name}:${image_tag}

if [ "${POWER}" = "YES" ]; then
    echo "Building POWER image"
    docker buildx build --platform linux/ppc64le --push -t "${full_image_name}" .
else
    echo "Building x86 image"
    docker build -t "${full_image_name}" .
    docker push "${full_image_name}"
fi
# build docker image
# docker build -t "${full_image_name}" .

# push docker image
# docker push "${full_image_name}"

# output the image digest, which contains immutable information about the built image
docker inspect --format='{{index .RepoDigests 0}}' "${full_image_name}"