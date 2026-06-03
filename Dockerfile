# syntax = docker/dockerfile:1

## Uncomment the version of python you want to test against
# FROM python:3.11-slim
# FROM python:3.12-slim
FROM python:3.13-slim
# FROM python:3.14-slim

# Set the working directory to /app
WORKDIR /app/

# Copy and install the requirements
# This includes egg installing the pamda package
COPY pamda/__init__.py /app/pamda/__init__.py
COPY pyproject.toml /app/pyproject.toml
RUN pip install -e .[dev]

# Drop into a shell by default
CMD ["/bin/bash"]
