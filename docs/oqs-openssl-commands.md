# Signing data

For creating signed data, two steps are required: One is the creation of a certificate using a QSC algorithm; the second is the use of this certificate (and its signature algorithm) to create the signed data:

## Step 1: Create quantum-safe key pair and self-signed certificate:

```
openssl req -x509 -new -newkey dilithium3 -keyout qsc.key -out qsc.crt -nodes -subj "/CN=oqstest" -days 365 -config /usr/lib/ssl/openssl.cnf -provider-path ~/oqs-provider/_build/oqsprov -provider oqsprovider -provider default
```

## Step 2: Sign data:

As the CMS standard requires the presence of a digest algorithm, while quantum-safe crypto does not, in difference to the QSC certificate creation command above, passing a message digest algorithm via the -md parameter is mandatory.

```
openssl cms -in inputfile -sign -signer qsc.crt -inkey qsc.key -nodetach -outform pem -binary -out signedfile -md sha512 -provider-path ~/oqs-provider/_build/oqsprov  -provider default -provider oqsprovider
```

Data to be signed is to be contained in the file named inputfile. The resultant CMS output is contained in file signedfile. The QSC algorithm used is the same signature algorithm utilized for signing the certificate qsc.crt.

---------------------

# Verifying data

Continuing the example above, the following command verifies the CMS file signedfile and outputs the outputfile. Its contents should be identical to the original data in inputfile above.

```
openssl cms -verify -CAfile qsc.crt -inform pem -in signedfile -crlfeol -out outputfile -provider-path ~/oqs-provider/_build/oqsprov -provider oqsprovider -provider default
```

# Extract public key

The public key can be extracted from the certificate using standard openssl command:

```
openssl x509 -provider-path ~/oqs-provider/_build/oqsprov -provider oqsprovider -provider default -in qsc.crt -pubkey -noout > qsc.pubkey
```

# openssl dgst

Also tested to operate OK is the openssl dgst command. Sample invocations building on the keys and certificate files in the examples above:

# Signing
```
openssl dgst -provider-path ~/oqs-provider/_build/oqsprov -provider oqsprovider -provider default -sign qsc.key -out dgstsignfile inputfile
```

# Verifying

```
openssl dgst -provider-path ~/oqs-provider/_build/oqsprov -provider oqsprovider -provider default -signature dgstsignfile -verify qsc.pubkey inputfile
```

# Convert PEM to DER
```
openssl x509 -in qsc.crt -outform DER -out qsc.der -provider-path ~/oqs-provider/_build/oqsprov -provider oqsprovider -provider default
```
