FROM ubuntu:16.04
MAINTAINER Chie HAYASHIDA <chie-hayashida@cookpad.com>

# apt-get
RUN apt-get update && apt-get install -y \
    git \
    vim \
    wget \
    curl \
    python3.5 \
    python3-pip \
    python3-dev \
    sudo

RUN pip3 install --upgrade pip
COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

# settings
ARG user_name=ubuntu
ARG user_id=2000
ARG group_name=ubuntu
ARG group_id=2000

# create user
RUN groupadd -g ${group_id} ${group_name}
RUN useradd -u ${user_id} -g ${group_id} -d /home/${user_name} --create-home --shell /bin/bash ${user_name}
RUN echo "${user_name} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R ${user_name}:${group_name} /home/${user_name}

ENV PYTHONUNBUFFERED 1

RUN apt-get install -y \
    python3.5 \
    python3-pip \
    python3-dev

# user settings
user ubuntu
workdir /work
ENV HOME /home/ubuntu
ENV LANG en_US.UTF-8
ENV LC_ALL="C"

copy docker/start.sh $home/

# Set alias for python3.5
RUN echo "alias python=python3" >> $HOME/.bashrc && \
    echo "alias pip=pip3" >> $HOME/.bashrc

# start jupyter lab
expose 8888
cmd ["bash", "start.sh"]
# cmd ["/bin/bash"]
