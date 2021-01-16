# Use an official Python runtime as a parent image
FROM aidocdev/ubuntu-conda

# install aws cli
RUN curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
RUN unzip awscli-bundle.zip
RUN ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

COPY environment.yml /app/environment.yml
RUN conda env create -f /app/environment.yml