# Use an official Python runtime as a parent image
FROM aidocdev/aidoc-demo-base

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY docker/app/instance /app/instance
COPY docker/app/credentials /root/.aws/credentials
COPY docker/app/pip.conf /root/.pip/pip.conf

# create demo conda environment
RUN conda env update -f environment.yml


# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run app.py when the container launches
CMD ["/app/docker/app/run_demo_server.sh"]