# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /ai-service

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

#  Copy the ./ai-service directory inside the /code directory.
COPY . /ai-service

# Expose the port on which the server will run
EXPOSE 8080

# Start the server using Uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]