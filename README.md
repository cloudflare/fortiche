# Fortiche

> Fortran compiler for Cloudflare Workers

## Usage

```
$ docker run -v $PWD:/input -v $PWD/output:/output xtuc/fortiche test.f90
```

Help:
```
$ docker run xtuc/fortiche --help

usage: fortiche [-h] [--export-func EXPORT_FUNC] [--with-BLAS-3-12-0]
                [--with-LAPACK-3-12-0] [--stack-size STACK_SIZE] [--verbose]
                files [files ...]

Fortran compiler for Cloudflare Workers

positional arguments:
  files                 Fortan source files

options:
  -h, --help            show this help message and exit
  --export-func EXPORT_FUNC
                        Fortran subroutine(s) to be exported to JavaScript
  --with-BLAS-3-12-0    Compile with BLAS 3.12.0
  --with-LAPACK-3-12-0  Compile with LAPACK 3.12.0
  --stack-size STACK_SIZE
                        Stack size (default: 4Mb)
  --verbose             Enable verbose mode
```

## Demos

- Simple: [add].
- More complex: [handwritten-digit-classifier].

[add]: ./examples/add
[handwritten-digit-classifier]: ./examples/handwritten-digit-classifier
