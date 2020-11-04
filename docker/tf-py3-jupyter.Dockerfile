ARG DOCKER_ENV=latest

FROM tensorflow/tensorflow:${DOCKER_ENV}
# DOCKER_ENV are specified again because the FROM directive resets ARGs
# (but their default value is retained if set previously)

ARG DOCKER_ENV

# disable tzdata questions
ENV DEBIAN_FRONTEND=noninteractive

# use bash
SHELL ["/bin/bash", "-c"]

# install apt-utils
RUN apt-get update -y \
  && apt-get install -y apt-utils 2> >( grep -v 'debconf: delaying package configuration, since apt-utils is not installed' >&2 ) \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update -q \
  && apt-get install -y libsm6 libxext6 libxrender-dev \
  && apt-get install -y git neovim graphviz \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install and update deps
RUN pip install --upgrade pip \
  && git clone https://github.com/ulises-jeremias/tf2-tools.git /tf/lib/tf2-tools \
  && pip3 install -e /tf/lib/tf2-tools

ADD requirements.txt .
RUN pip3 install -r requirements.txt
