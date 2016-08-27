cfg-wcec-sim
============

## Dependency

* python 2.7.6

## Install

```bash
$ bash setup.sh
```

## Run

### Study Case I

```bash
$ python run.py study-case-I-three-tests/sim.config wfreq 20 ./study-case-I/results
$ python run.py study-case-I-three-tests/sim.config valentin 20 ./study-case-I/results
$ python run.py study-case-I-three-tests/sim-mine.config mine 20 ./study-case-I/results
$ bash ./study-case-I/gnuplot/run.sh # generate graphs
```

or simply do '$ bash run.sh' that encapsulate all that commands.

### Study Case II

```bash
$ python run.py study-case-II-eight-tests/sim.config
$ python run.py study-case-II-eight-tests/sim-mine.config
```

or change 'run.sh' and do:

```bash
$ ./run.sh
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
$ sed -i -e 's/usr\/local\/akaroa/opt\/akaroa-2\.7\.13/g' src/Makefile.am
$ sed -i -r 's/if \(almostequal2s_complement\(Ip, Ipa, 1 << 22\)\)/if \(Ip <= Ipa \&\& Ip >= Ipa\)/g' src/analysis.c
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

