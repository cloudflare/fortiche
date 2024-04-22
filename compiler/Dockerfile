FROM ubuntu:23.10 as builder

RUN apt-get update
RUN apt-get -y install cmake git build-essential ninja-build python3 clang

WORKDIR /llvm

COPY ./deps/llvm-project ./deps/llvm-project

COPY ./extend-flang-target.patch .
COPY ./force-4-byte-values.diff .

RUN git apply ./extend-flang-target.patch
RUN git apply ./force-4-byte-values.diff

RUN cmake -G Ninja -S deps/llvm-project/llvm -B build \
    -DCMAKE_INSTALL_PREFIX=llvm-18.1.1 \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DLLVM_DEFAULT_TARGET_TRIPLE="wasm32-unknown-emscripten" \
    -DLLVM_TARGETS_TO_BUILD="WebAssembly" \
    -DLLVM_ENABLE_PROJECTS="clang;flang;mlir"

# I'm running out of memory if I go above ~13 cores. 13 cores uses swap already.
RUN cmake --build build --parallel 13

WORKDIR /emsdk

COPY ./deps/emsdk .

# enable emscripten
RUN ./emsdk install latest
RUN ./emsdk activate latest

# source emsdk
ENV PATH /emsdk:/emsdk/node/16.20.0_64bit/bin:/emsdk/upstream/emscripten:/emsdk/upstream/bin:$PATH
ENV EMSDK /emsdk
ENV EM_CONFIG /root/.emscripten

WORKDIR /binaryen

RUN git clone --recursive https://github.com/WebAssembly/binaryen.git .

RUN cmake .
RUN make -j$(nproc) wasm-opt install

# libFortranRuntime.a
ENV PATH /binaryen:$PATH

WORKDIR /libfortranruntime

COPY ./deps/libfortranruntime .
RUN make -j$(nproc) build

# Warmup emscripten cache
RUN /emsdk/upstream/emscripten/embuilder.py build MINIMAL

WORKDIR /BLAS

COPY ./deps/BLAS-3.12.0 .
RUN make FC=/llvm/build/bin/flang-new FFLAGS=-O2 FFLAGS_NOOPT=-O0 AR=emar RANLIB=emranlib -j$(nproc)

WORKDIR /lapack

COPY ./deps/lapack-3.12.0 .
RUN cp -v make.inc.example make.inc
RUN make FC=/llvm/build/bin/flang-new FFLAGS=-O2 FFLAGS_DRV=-O2 FFLAGS_NOOPT=-O0 AR=emar RANLIB=emranlib TIMER=INT_CPU_TIME -j$(nproc) lib

WORKDIR /compiler

COPY ./pre-em.js .
COPY ./fortiche.py .

ENTRYPOINT ["python3", "/compiler/fortiche.py"]
