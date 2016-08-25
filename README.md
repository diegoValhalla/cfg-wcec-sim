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
$
$ echo '
3 5 1
1000 800 600 400 150
1.8 1.6 1.3 1 0.75
10707 30 0.4 0
9563 40 0.4 0
13951 60 0.4 0' > in
$
$ ./bin/se -s < in
Sumário
Número de Configurações:    125
Configurações Avaliadas:    125
Configurações Viáveis: 4
Tempo de processamento: 0s and 448 us
Melhor espalhamento 36.16 com as seguintes frequências
(1000.00; 1.80) (800.00; 1.60) (1000.00; 1.80)
Utilização total do sistema é  88.83%
Energia gasta pelo sistema é 104373.20 x C
Energia gasta pelo sistema é 110876.04 x C se usar apenas a maior frequência
Redução de energia:   5.86%
```

