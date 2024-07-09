# OpenSSL oqsprovider usage
 
This document describes how to generate keypairs, CSR, and certificates using oqsprovider.
`oqsprovider` is an external OpenSSL provider that implements post quantum cryptographical algorithms. `oqsprovider` must be built before usage.

In this project `oqsprovider` is used to 

- generate dilithium keypair
- generate csr (optional)
- self-sign certificate OR sign certificate using CA created for the project.

## Tutorial

Start by defining environment variable in the shell
```
export PROVIDERPATH="/home/user/oqs-provider/_build/oqsprov"
```

Commands are standard openssl commands with the addition of loading the provider.
Add `-provider-path=$PROVIDERPATH -provider oqsprovider -provider default` to every command.
Note that once you have loaded a provider into a library context the default provider is not automatically loaded (as usual), thus the default provider needs to be explicitly loaded as well.

### Creating private key
```
openssl genpkey -out pqc.key -algorithm dilithium3 -provider-path $PROVIDERPATH -provider oqsprovider -provider default
```
If you want to encrypt the key add `-aes-256-cbc` and prompt a password.

### Creating CSR (or signing without interactive csr) (OPTIONAL...)


### Self signing certificate
- this command will create certificate from keypair without CSR (prompt will open and ask questions)
```
openssl req -new -x509 -key pqc.key -out my.crt -days 365 -provider-path $PROVIDERPATH -provider oqsprovider -provider default
```

- check certificate information
```
openssl x509 -text -in mypqc.crt -noout -provider-path $PROVIDERPATH -provider oqsprovider -provider default
```

### Sign certificate with CA
TODO
