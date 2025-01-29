docker build . --tag "pamda" --quiet
docker run -it --rm \
    --volume "$(pwd):/app" \
    "pamda"

