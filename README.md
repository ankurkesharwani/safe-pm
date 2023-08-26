# safe-password-manager
A simple open-source password manager that you can trust

# Proposed API

## Create a password db

```
$ safe-pm setup --name <DB_NAME>
```

## Store operations

```
$ safe-pm store create --db <DB_NAME> --name <STORE_NAME>
```

```
$ safe-pm store rename --db <DB_NAME> --oldname <OLD_STORE_NAME> --newname <NEW_STORE_NAME> 
```

```
$ safe-pm store delete --db <DB_NAME> --name <STORE_NAME>
```

## Account operations

```
$ safe-pm account list --db <DB_NAME> --store <STORE_NAME>
```

```
$ safe-pm account create \
    --db <DB_NAME> \
    --store <STORE_NAME> \
    --name <ACCOUNT_NAME> \
    --username <USERNAME> \
    --password <PASSWORD TO USE>

or

$ safe-pm account create \
    --db <DB_NAME> \
    --store <STORE_NAME> \
    --name <ACCOUNT_NAME> \
    --username <USERNAME> \
    --auto-gen-password \
    --pass-min-length <MIN_LENGTH> \
    --pass-max-length <MAX_LENGTH> \
    --pass-no-special \
    --pass-no-digits \
    --pass-exclude-chars <CHARS_TO_EXCLUDE> \
```

```
$ safe-pm account view --db <DB_NAME> --store <STORE_NAME> --name <ACCOUNT_NAME> 
```

```
$ safe-pm account copy --db <DB_NAME> --store <STORE_NAME> --name <ACCOUNT_NAME> 
```

```
$ safe-pm account update \
    --db <DB_NAME> \
    --store <STORE_NAME> \
    --name <ACCOUNT_NAME> \
    --password <PASSWORD TO USE>

or

$ safe-pm account update \
    --db <DB_NAME> \
    --store <STORE_NAME> \
    --name <ACCOUNT_NAME> \
    --auto-gen-password \
    --pass-min-length <MIN_LENGTH> \
    --pass-max-length <MAX_LENGTH> \
    --pass-no-special
    --pass-no-digits
    --pass-exclude-chars <CHARS_TO_EXCLUDE>
```

```
$ safe-pm account delete --db <DB_NAME> --store <STORE_NAME> --name <ACCOUNT_NAME> 
```

```
$ safe-pm account history --db <DB_NAME> --store <STORE_NAME> --name <ACCOUNT_NAME> 
```