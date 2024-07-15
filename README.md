# BB84 Authentication

This repository contains authentication software to use on the quantum link layer in BB84 QKD protocol.

Authentication is implemented using PQC primitives implemented in open-source libraries liboqs and oqsprovider. More information on liboqs and oqs-provider [here](https://openquantumsafe.org/).

## Getting started

### NOTE: 

This software is tested using versions [liboqs=0.7.2](https://github.com/open-quantum-safe/liboqs/releases/tag/0.7.2)
and [oqsprovider=0.4.0](https://github.com/open-quantum-safe/oqs-provider/releases/tag/0.4.0) on system running Ubuntu 22.04 with OpenSSL version 3.0.2.
This software is not guaranteed to work with other versions of liboqs, oqsprovider and OpenSSL.

## Step 1: Building liboqs:

Example for building and installing liboqs in `.local`:

```
    wget https://github.com/open-quantum-safe/liboqs/archive/refs/tags/0.7.2.zip
    unzip 0.7.2.zip
    cd liboqs-0.7.2
    sudo cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local -S . -B _build
    sudo cmake --build _build && sudo cmake --install _build
    cd ..
```

## Step 2: Building oqsprovider:

`oqsprovider` can be built for example via the following:

```
    wget https://github.com/open-quantum-safe/oqs-provider/archive/refs/tags/0.4.0.zip
    unzip 0.4.0.zip
    cd oqs-provider-0.4.0
    cmake -DOPENSSL_ROOT_DIR=~/.local -DCMAKE_PREFIX_PATH=~/.local -S . -B _build
    cmake --build _build
```

## Step 3: Test the functionality of the libraries

```
    cd ..
    mkdir oqs-test && cd oqs-test
    export PROVIDERPATH="/home/user/oqs-provider-0.4.0/_build/oqsprov"
    openssl genpkey -out pqc.key -algorithm dilithium3 -provider-path $PROVIDERPATH -provider oqsprovider -provider default
```

## Step 4: install liboqs-python 0.7.2

```
    wget https://github.com/open-quantum-safe/liboqs-python/archive/refs/tags/0.7.2.zip
    unzip 0.7.2.zip
    python3 -m venv venv
    source venv/bin/activate
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
    cd liboqs-python-0.7.2
    python3 setup.py install
```

## Step 4: Clone this repository

TODO instructions.

## What is in this repository

Directory `signature_authentication` contains authentication software demo using post-quantum digital signature scheme CRYSTALS-Dilithium.

## Note: Before using

Create private key and certificate for Alice and Bob on their respective laptops:

```
cd dilithium_sign
python gen_auth_keys.py alice
```

This creates private key  `alice.key` and certificate `alice.der` in DER format to directory
`dilithium_sign/tmp/`.
If `tmp/` directory does not exist script creates it.
