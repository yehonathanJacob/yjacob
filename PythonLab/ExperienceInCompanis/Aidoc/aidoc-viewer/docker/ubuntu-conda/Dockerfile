# Use an official Python runtime as a parent image
FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
  bzip2 \
  wget \
  vim \
  curl \
  unzip

#Install miniconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh
RUN ./Miniconda3-latest-Linux-x86_64.sh -b -p

ENV PATH="/root/miniconda3/bin/:$PATH"