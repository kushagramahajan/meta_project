#!/bin/bash
set -e

# openface
git clone --depth 1 https://github.com/TadasBaltrusaitis/OpenFace.git
cd OpenFace
bash download_models.sh
export openface_version=$(git log -1 --format='%cd.%h' --date=short | tr -d -)
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_CXX_FLAGS=-march=native -D CMAKE_INSTALL_PREFIX=$HOME/local ..
make
make install
cd ../..
rm -rf OpenFace
