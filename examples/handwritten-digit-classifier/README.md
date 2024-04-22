# How to deploy

## Compile Fortran

```
docker run -v $PWD:/input -v $PWD/output:/output xtuc/fortiche --export-func=classifier --with-BLAS-3-12-0 classifier.f90
```

## Publish Worker

```
wrangler deploy
```
