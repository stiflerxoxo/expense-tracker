# Use the official lightweight Nginx image
FROM nginx:1.27-alpine

# Copy your custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set the working directory to the default Nginx web root directory
WORKDIR /usr/share/nginx/html

# Copy all your frontend assets (HTML, CSS, JS) directly into the web root
COPY index.html .
COPY css/ ./css
COPY js/ ./js

# Document that the web server runs on port 80
EXPOSE 80























# # Use version 3.8 of the Docker Compose template format
# version: '3.8'

# services:

#   # --- 1. DATABASE CONTAINER ---
#   db:
#     # Download a clean, tiny PostgreSQL database image from the internet
#     image: postgres:16-alpine
#     environment:
#       # Set up the master login username for your database
#       - POSTGRES_USER=expense_user
#       # Set up the secure login password for your database
#       - POSTGRES_PASSWORD=12345
#       # Create an empty starter database folder named "expense_db"
#       - POSTGRES_DB=expense_db

#   # --- 2. PYTHON FASTAPI BACKEND CONTAINER ---
#   backend:
#     # Go into the local /backend directory and build it using its Dockerfile
#     build: ./backend
#     ports:
#       # Link port 8000 on your computer to port 8000 inside the container
#       - "8000:8000"
#     environment:
#       # Pass the database username to the Python application code
#       - POSTGRES_USER=expense_user
#       # Pass the database password to the Python application code
#       - POSTGRES_PASSWORD=12345
#       # Tell the Python code which database folder to connect to
#       - POSTGRES_DB=expense_db
#       # Tell the Python code that the database is running inside the "db" container
#       - POSTGRES_HOST=db
#       # Use the default network port required to talk to PostgreSQL
#       - POSTGRES_PORT=5432
#     depends_on:
#       # Wait for the database container to launch before starting the backend api
#       - db

#   # --- 3. NGINX WEB FRONTEND CONTAINER ---
#   frontend:
#     # Go into the local /frontend directory and build it using its Dockerfile
#     build: ./frontend
#     ports:
#       # Map port 8080 on your machine so you can open http://localhost:8080 in your browser
#       - "8080:80"
#     depends_on:
#       # Wait for the backend container to launch before starting this web front interface
#       - backend












# version: '3.8' # Uses version 3.8 of the Docker Compose format

# services:
#   # 1. DATABASE SERVICE
#   db:
#     image: postgres:16-alpine # Downloads a clean, lightweight PostgreSQL database image
#     environment:
#       - POSTGRES_USER=expense_user # Sets the database admin username
#       - POSTGRES_PASSWORD=12345 # Sets the password to lock/unlock the database
#       - POSTGRES_DB=expense_db # Creates a new database named "expense_db"

#   # 2. PYTHON FASTAPI BACKEND SERVICE
#   backend:
#     build: ./backend # Looks inside the /backend folder and runs its Dockerfile
#     ports:
#       - "8000:8000" # Links port 8000 on your computer to port 8000 inside the container
#     environment:
#       - POSTGRES_USER=expense_user # Tells the code which username to use to log in
#       - POSTGRES_PASSWORD=12345 # Tells the code the password to log in
#       - POSTGRES_DB=expense_db # Tells the code which database folder to read
#       - POSTGRES_HOST=db # Connects the backend to the database service named "db" above
#       - POSTGRES_PORT=5432 # Uses the default internal port for PostgreSQL
#     depends_on:
#       - db # Forces Docker to start the database ("db") BEFORE starting this backend

#   # 3. NGINX WEB FRONTEND SERVICE
#   frontend:
#     build: ./frontend # Looks inside the /frontend folder and runs its Dockerfile
#     ports:
#       - "8080:80" # Opens your browser app at http://localhost:8080
#     depends_on:
#       - backend # Forces Docker to start the backend API BEFORE starting this webpage
