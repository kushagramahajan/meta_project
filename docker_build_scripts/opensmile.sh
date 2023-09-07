#!/bin/bash
set -e

git clone https://github.com/audeering/opensmile.git
cd opensmile
export opensmile_version=$(git log -1 --format='%cd.%h' --date=short | tr -d -) 
bash build.sh
mkdir -p $HOME/local/share/opensmile
cp build/progsrc/smilextract/SMILExtract $HOME/local/bin/
cp -r config $HOME/local/share/opensmile/
cp -r scripts $HOME/local/share/opensmile/
cd ..
rm -rf opensmile
sed -i "s/frameMode = full/frameMode = \\\cm[frameMode{center}:frameMode]/" $HOME/local/share/opensmile/config/shared/FrameModeFunctionals.conf.inc
sed -i "s/frameSize = 0/frameSize = \\\cm[frameSize{4}:frameSize]/" $HOME/local/share/opensmile/config/shared/FrameModeFunctionals.conf.inc
sed -i "s/frameStep = 0/frameStep = \\\cm[frameStep{0.1}:frameStep]/" $HOME/local/share/opensmile/config/shared/FrameModeFunctionals.conf.inc
sed -i "s/frameCenterSpecial = left/frameCenterSpecial = center/" $HOME/local/share/opensmile/config/shared/FrameModeFunctionals.conf.inc
