# use official Python image as base
FROM python:3.11-slim

# set working directory inside the container
WORKDIR /app

# copy requirements first (so Docker caches this layer)
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of your code
COPY . .

# expose the port FastAPI runs on
EXPOSE 8000

# command to start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]