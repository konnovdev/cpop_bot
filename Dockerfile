FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-dev zlib1g-dev libjpeg-turbo8-dev libwebp-dev pip
VOLUME /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
CMD python3 tgbot.py

# Notice: if the file `requirements.txt` is changed - the image needs to be rebuilt.
# To rebuild the image using `docker-compose` just add `--build` flag like this:
# `docker-compose up -d --build`

# The steps in this Dockerfile are the following:
# 1) Getting a base ubuntu image.
#
# 2) Starting the image build process by running
# installation of python and ubuntu modules required.
#
# 3) Mounting a volume to a directory in the container /usr/src/app.
# The host directory will be specified as the current directory in docker-compose.yml
#
# 4) Copying the python requirements file to the specified directory
#
# 5) Installing all the libraries specified in the requirements file. This is the last step
# of the build process.
#
# 6) Launching the container by running a bot with `python3 tgbot.py` (this is NOT a part
# of the build step)