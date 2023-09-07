# build: podman build --tag image --file image.dockerfile .
# for singularity
# 1) export: podman save --format=docker-archive -o image.docker localhost/image
# 2) import: singularity build image.sif docker-archive://image.docker
# 3) run: singularity shell image.sif
# for toolbox
# 1) toolbox create --image localhost/image image
# 2) toolbox enter image

FROM python:3.9-bookworm

COPY openface.sh /openface.sh
COPY opensmile.sh /opensmile.sh

RUN cd /
RUN sed -i 's/\$HOME/\/usr/g' openface.sh
RUN sed -i 's/\$HOME/\/usr/g' opensmile.sh
RUN sed -i 's/-march=native/-march=haswell/g' openface.sh
RUN sed -i 's/-march=native/-march=haswell/g' opensmile.sh

# build in parallel
RUN export MAKEFLAGS="-j`nproc`"

# update
RUN export DEBIAN_FRONTEND=noninteractive
RUN sed -i'' -e 's/main$/main non-free/g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update && apt-get -y upgrade 

RUN apt install --no-install-recommends -y \
 vim openssh-client npm nodejs \
 python3-pip python3-dev python3-numpy \
 build-essential cmake pkg-config autotools-dev automake ca-certificates m4 gcc g++ libtool \
 git unzip wget p7zip-full p7zip-rar \
 ffmpeg libsndfile1 \
 libxt-dev libnss3 libasound2 libxtst6 libcap2 \
 libopencv-dev python3-opencv libopenblas-dev libdlib-dev \
 libncurses-dev \
 r-base-dev r-base r-recommended libharfbuzz-dev libfribidi-dev \
 texlive texlive-latex-extra texlive-fonts-recommended dvipng cm-super

# for python development
RUN python3 -m pip install black ruff ruff-lsp poetry

# for coc-pyright
RUN npm install -g yarn
RUN npm install -g pyright

# OpenFace, openSMILE
RUN . ./openface.sh
RUN . ./opensmile.sh

# remove copied files
RUN rm opensmile.sh openface.sh

# remove some build tools
RUN apt -y autoremove
RUN apt -y clean
RUN apt -y autoclean
RUN rm -rf /tmp/*
RUN rm -rf /var/cache/apt/archives/*

RUN mkdir -p /.singularity.d/env/
ARG PROFILE=/.singularity.d/env/99-zz-profile.sh
RUN echo '#!/bin/bash' > $PROFILE
RUN echo "if [ -e \$HOME/.profile ]; then" >> $PROFILE
RUN echo "    . \$HOME/.profile" >> $PROFILE
RUN echo "elif [ -e \$HOME/.bash_profile ]; then" >> $PROFILE
RUN echo "    . \$HOME/.bash_profile" >> $PROFILE
RUN echo "fi" >> $PROFILE
RUN echo "PS1=\"singularity \$PS1\"" >> $PROFILE
RUN chmod 755 $PROFILE


# adding Mediapipe and HR functionality

ARG HOME_DIR=/home
ARG HR_DIR=/home/rPPG-Toolbox
ARG POSE_DIR=/home/Mediapipe-Pose
RUN pip install mediapipe
WORKDIR ${HOME_DIR}
RUN mkdir ${HR_DIR}
RUN mkdir ${POSE_DIR}
RUN ls ${HOME_DIR}
ADD rPPG-Toolbox /home/rPPG-Toolbox
ADD mediapipe_pose.py /home/Mediapipe-Pose
RUN chmod -R 777 /home/rPPG-Toolbox/output_files

RUN pip install h5py yacs pandas scikit_image matplotlib PyYAML==6.0 scikit-learn tqdm mat73 scipy==1.6 torch==1.12.1 torchvision==0.13.1 numpy==1.22.0

ENTRYPOINT ["/bin/bash"]