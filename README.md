cfg-wcec-sim
============

## Install

```bash
$ bash setup.sh
```

## Run

Each execution result is stored in 'data/' directory with the same file name.
So, in each running, you should change file name to avoid overwrite data.

### Study Case I

```bash
$ python run.py study-case-I-three-tests/sim.config
$ python run.py study-case-I-three-tests/sim-mine.config
```

### Study Case II

```bash
$ python run.py study-case-II-eight-tests/sim.config
$ python run.py study-case-II-eight-tests/sim-mine.config
```

## Tools

### cfg-wcec

```bash
$ git submodule init
$ git submodule update
$ bash ./tools/cfg-wcec/setup.sh
$ mkdir ${SETUP_DIR}/data
```

### smartenum

```bash
$ git clone git://repo.or.cz/smartenum.git
$ cd smartenum
$ sudo apt-get install autoconf automake
$ sudo tar -xzf akaroa-2.7.13.tar.gz -C /opt/akaroa-2.7.13
$ autoreconf -i
$ ./configure --bindir=/home/diego/projects/smartenum/bin
$ make
$ make install
```

