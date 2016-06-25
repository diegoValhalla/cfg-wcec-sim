SETUP_DIR=$(dirname `readlink -f $0`)

git submodule init
git submodule update
bash ./tools/cfg-wcec/setup.sh
mkdir ${SETUP_DIR}/data
