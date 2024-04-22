# How to deploy

## Compile Fortran

```
docker run -v $PWD:/input -v $PWD/output:/output xtuc/fortiche --export-func=add add.f90
```

## Publish Worker

```
wrangler deploy
```
