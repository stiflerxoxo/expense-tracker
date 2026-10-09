### STAGE 1: install packages ###
# Use Python 3.12 (slim version) and call this step "build"
FROM python:3.12-slim AS build

# Create a folder named /app and move into it
WORKDIR /app

# Create a blank Python virtual environment folder named /venv
RUN python -m venv /venv

# Tell the system to use the Python inside our new /venv folder
ENV PATH="/venv/bin:$PATH"

# Copy your requirements.txt file from your computer into the container
COPY requirements.txt .

# Install all your python packages without saving useless installer files
RUN pip install --no-cache-dir -r requirements.txt


### STAGE 2: final image ###
# Start fresh with a clean, empty Python 3.12 image
FROM python:3.12-slim

# Create a folder named /app and move into it
WORKDIR /app

# Copy ONLY the finished /venv folder from the "build" step into this clean image
COPY --from=build /venv /venv

# Tell this new container to use the Python inside our copied /venv folder
ENV PATH="/venv/bin:$PATH"

# Copy your actual "app" code folder from your computer into the container
COPY app ./app

# Label the container to show it uses port 8000
EXPOSE 8000

# Run your app using Uvicorn when the container starts up
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
