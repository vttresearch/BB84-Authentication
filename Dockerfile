FROM ubuntu:22.04

WORKDIR /usr/src/app

# Copy the contents of this repository to the container
COPY . .

# Step 1: Build liboqs
RUN apt update && apt install -y wget zip python3 python3-venv astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind
RUN wget https://github.com/open-quantum-safe/liboqs/archive/refs/tags/0.7.2.zip
RUN unzip 0.7.2.zip
RUN cd liboqs-0.7.2 && cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local -S . -B _build && cmake --build _build && cmake --install _build

# Step 2: build oqsprovider
RUN cd ..
RUN wget https://github.com/open-quantum-safe/oqs-provider/archive/refs/tags/0.4.0.zip
RUN unzip 0.4.0.zip
RUN cd oqs-provider-0.4.0 && cmake -DOPENSSL_ROOT_DIR=/usr/local -DCMAKE_PREFIX_PATH=/usr/local -S . -B _build && cmake --build _build

# Step 3: build liboqs-python
RUN cd ..
RUN apt install -y python3-pip && pip install setuptools
RUN wget https://github.com/open-quantum-safe/liboqs-python/archive/refs/tags/0.7.2.zip
RUN unzip 0.7.2.zip.1
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
RUN cd liboqs-python-0.7.2 && python3 setup.py install

# Start script
RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]

CMD ["alice"]
