IF_VER_GE = $(shell test "$1" -ge "$2" && echo YES)
VER = $(shell gfortran -dumpversion | cut -d"." -f1)

ifeq "$(call IF_VER_GE, $(VER), 12)" "YES"
    FLAGS = -fallow-argument-mismatch
else
    FLAGS =
endif

all: libcnufft.so

clean:
	rm -f *.o *.so _cnufft.c cwrap_nufft.mod

libfnufft.so:
	gfortran -c -fPIC ./src/dfftpack.f -o dfftpack.o ${FLAGS}
	gfortran -c -fPIC ./src/next235.f -o next235.o
	gfortran -c -fPIC ./src/nufft1df90.f -o nufft1df90.o
	gfortran -c -fPIC ./src/nufft2df90.f -o nufft2df90.o
	gfortran -c -fPIC ./src/nufft3df90.f -o nufft3df90.o
	gfortran -o $@ --shared -fPIC \
		dfftpack.o \
		next235.o \
		nufft1df90.o \
		nufft2df90.o \
		nufft3df90.o \
		cwrapfor.f90

libcnufft.so: cnufft.o libfnufft.so
	gcc --shared $^ -o $@

cnufft.o:
	gcc -c -Wall -fpic cnufft.c

# nufft: export LD_LIBRARY_PATH = $(shell pwd)
# nufft: libnufft.so
# 	./nufft_build.py
