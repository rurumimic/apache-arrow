# CUDA

- [Python Development](https://arrow.apache.org/docs/developers/python.html)
- docker
  - [nvidia/cuda](https://hub.docker.com/r/nvidia/cuda)
  - [GPU support in Docker Desktop](https://docs.docker.com/desktop/gpu/)
- ref
  - [Building pyarrow with CUDA support](https://randyzwitch.com/pyarrow-cuda-support/)

## cuDF

- github: [rapidsai/cudf](https://github.com/rapidsai/cudf)

```bash
python -V # 3.10.z
pip install --extra-index-url=https://pypi.nvidia.com cudf-cu12
```

## Build Arrow

```bash
git clone https://github.com/apache/arrow.git
cd arrow
git submodule init
git submodule update
git checkout apache-arrow-15.0.2
export PARQUET_TEST_DATA="${PWD}/cpp/submodules/parquet-testing/data"
export ARROW_TEST_DATA="${PWD}/testing/data"
```

```bash
pyenv virtualenv 3.11.z pyarrow
pyenv activate pyarrow
pip install -U pip setuptools
pip install six numpy pandas cython pytest hypothesis
mkdir dist
export ARROW_HOME=$(pwd)/dist
export LD_LIBRARY_PATH=$(pwd)/dist/lib:$LD_LIBRARY_PATH
```

```bash
ARROW_THIRDPARTY=/tmp/arrow-thirdparty

cd cpp
./thirdparty/download_dependencies.sh $ARROW_THIRDPARTY/arrow-thirdparty
```

```bash
export CC=gcc
export CXX=g++

mkdir build && cd build

cmake -DCMAKE_INSTALL_PREFIX=$ARROW_HOME \
-DCMAKE_INSTALL_LIBDIR=lib \
-DARROW_FLIGHT=OFF \
-DARROW_GANDIVA=ON \
-DARROW_ORC=ON \
-DARROW_WITH_BZ2=ON \
-DARROW_WITH_ZLIB=ON \
-DARROW_WITH_ZSTD=ON \
-DARROW_WITH_LZ4=ON \
-DARROW_WITH_SNAPPY=ON \
-DARROW_WITH_BROTLI=ON \
-DARROW_PARQUET=ON \
-DARROW_PYTHON=ON \
-DARROW_PLASMA=ON \
-DARROW_BUILD_TESTS=ON \
-DARROW_CUDA=ON \
-DARROW_COMPUTE=ON \
-DCMAKE_BUILD_TYPE=Debug \
-DARROW_BUILD_TESTS=ON \
-DARROW_COMPUTE=ON \
-DARROW_CSV=ON \
-DARROW_DATASET=ON \
-DARROW_FILESYSTEM=ON \
-DARROW_HDFS=ON \
-DARROW_JSON=ON \
-DPARQUET_REQUIRE_ENCRYPTION=ON \
..


make -j12
make install
```

...