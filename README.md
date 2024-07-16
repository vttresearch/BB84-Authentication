# BB84 Authentication Demo

This repository contains authentication software to use on the quantum link layer in BB84 QKD protocol.

Quantum safe authentication is implemented using PQC primitives.

## Getting started

### NOTE: 

This software has external dependencies.
The main dependencies are open-source libraries liboqs, liboqs-python and oqsprovider. More information on these libraries is available [here](https://openquantumsafe.org/).

This software is tested using versions [liboqs=0.7.2](https://github.com/open-quantum-safe/liboqs/releases/tag/0.7.2)
and [oqsprovider=0.4.0](https://github.com/open-quantum-safe/oqs-provider/releases/tag/0.4.0) 
and [liboqs-python=0.7.2](https://github.com/open-quantum-safe/liboqs-python/releases/tag/0.7.2)
on a system running Ubuntu 22.04 with OpenSSL version 3.0.2.
This software is not guaranteed to work with other versions of liboqs, liboqs-python, oqsprovider and OpenSSL.

Below some instructions on how to install these dependencies.

### Step 1: Building liboqs:

Example for building and installing liboqs in `/usr/local`:

```
    wget https://github.com/open-quantum-safe/liboqs/archive/refs/tags/0.7.2.zip
    unzip 0.7.2.zip
    cd liboqs-0.7.2
    sudo cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local -S . -B _build
    sudo cmake --build _build && sudo cmake --install _build
    cd ..
```

### Step 2: Building oqsprovider:

`oqsprovider` can be built for example via the following:

```
    wget https://github.com/open-quantum-safe/oqs-provider/archive/refs/tags/0.4.0.zip
    unzip 0.4.0.zip
    cd oqs-provider-0.4.0
    cmake -DOPENSSL_ROOT_DIR=~/.local -DCMAKE_PREFIX_PATH=~/.local -S . -B _build
    cmake --build _build
```

### Step 3: Test the functionality of the libraries

```
    cd ..
    mkdir oqs-test && cd oqs-test
    export PROVIDERPATH="/home/user/oqs-provider-0.4.0/_build/oqsprov"
    openssl genpkey -out pqc.key -algorithm dilithium3 -provider-path $PROVIDERPATH -provider oqsprovider -provider default
```

### Step 4: install liboqs-python 0.7.2

```
    wget https://github.com/open-quantum-safe/liboqs-python/archive/refs/tags/0.7.2.zip
    unzip 0.7.2.zip
    python3 -m venv venv
    source venv/bin/activate
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
    cd liboqs-python-0.7.2
    python3 setup.py install
```

### Step 5: Clone this repository

Clone this repository and see the section "Usage" below.

## What is in this repository

Directory `signature_authentication` contains authentication software demo using *only* post-quantum digital signature scheme CRYSTALS-Dilithium.

Directory `mac_authentication` contains authentication software demo using post-quantum key encapsulation algorithm Kyber and message authentication codes (`hmac`).

We recommend using the `mac_authentication` alternative, as it is tested to be more efficient.

**DISCLAIMER**: this repository does not contain any code to perform the actual BB84 key distillation with error correction and privacy amplification steps. The scripts in this repository are only used to demonstrate the quantum-safe authentication of the classical channel.

For more details on the contents of this repository and the topic in general, please refer to this [publication](https://cris.vtt.fi/en/publications/quantum-safe-authentication-of-quantum-key-distribution-protocol).

## Usage

This is how you launch the `mac_authentication` demo:

- Open a new terminal tab.
- Execute the commands below:

```
source venv/bin/activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
cd mac_authentication
python3 alice.py
```

This launches the `alice.py` program on port `localhost:65530`. Alice will wait connection from Bob.

- Now, open another terminal tab
- Execute the commands below:

```
source venv/bin/activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
cd mac_authentication
python3 bob.py
```

This launches the `bob.py` program which connects to Alice on `localhost:65530` and starts the authenticated "key distillation" over the classical channel.

Scripts use automatically created `./tmp/` directory for temporary file storage.
