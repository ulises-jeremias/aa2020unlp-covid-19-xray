# aa2020unlp-covid-19-xray

Kaggle Challenge to Classify Covid Pneumonia Xray

## Content

- [aa2020unlp-covid-19-xray](#aa2020unlp-covid-19-xray)
  - [Content](#content)
  - [Quickstart](#quickstart)
    - [Tags](#tags)
    - [Variants](#variants)
  - [Datasets](#datasets)

## Quickstart

To start the docker container execute the following command

```sh
$ ./bin/start [-n <string>] [-t <tag-name>] [--sudo] [--build] [-d] [-c <command>]
```

### Tags

- **latest**	The latest release of TensorFlow CPU binary image. Default.
- **nightly**	Nightly builds of the TensorFlow image. (unstable)
version	Specify the version of the TensorFlow binary image, for example: 2.1.0
- **devel**	Nightly builds of a TensorFlow master development environment. Includes TensorFlow source code.

### Variants

> Each base tag has variants that add or change functionality:

- **\<tag\>-gpu**	The specified tag release with GPU support. (See below)
- **\<tag\>-py3**	The specified tag release with Python 3 support.
- **\<tag\>-jupyter**	The specified tag release with Jupyter (includes TensorFlow tutorial notebooks)

You can use multiple variants at once. For example, the following downloads TensorFlow release images to your machine. For example:

```sh
$ ./bin/start -n myContainer --build  # latest stable release
$ ./bin/start -n myContainer --build -t devel-gpu # nightly dev release w/ GPU support
$ ./bin/start -n myContainer --build -t latest-gpu-jupyter # latest release w/ GPU support and Jupyter
```

Once the docker container is running it will execute the contents of the /bin/execute file.

You can execute

```sh
$ docker exec -it <container-id> /bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"
```
to access the running container's shell.

## Datasets

You will need the other datasets to use localted at `data/<dataset_name>/data` in order to generate the new dataset. Then, you can just run the following command in order to generate the new dataset.

```sh
$ python src/datasets/datagen/cli.py \
    --dataset aa2020 \
    --splits_dir ./data/aa2020/splits \
    --split v1 \
    --train_size 0.75 \
    --test_size 0.25 \
    --seed 40
```
