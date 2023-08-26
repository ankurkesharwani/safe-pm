# safe-password-manager
A simple open-source password manager that you can trust

# Proposed API

## Create a password db

```
$ safe-pm setup --name <DB_NAME>
```

## Store operations

```
$ safe-pm store create --name <STORE_NAME>
```

```
$ safe-pm store rename --oldname <OLD_STORE_NAME> --newname <NEW_STORE_NAME> 
```

```
$ safe-pm store delete --name <STORE_NAME>
```

## Account operations

```
$ safe-pm account create \
    --store <STORE_NAME> \
    --name <ACCOUNT_NAME> \
    --username <USERNAME> \
    --password <PASSWORD TO USE>

or

$ safe-pm account 
    --create \
    --store <STORE_NAME> \
    --name <ACCOUNT_NAME> \
    --username <USERNAME> \
    --auto-gen-password \
    --pass-min-length <MIN_LENGTH> \
    --pass-max-length <MAX_LENGTH> \
    --pass-no-special
    --pass-no-digits
    --pass-exclude-chars <CHARS_TO_EXCLUDE>
```

```
$ safe-pm account --view --store <STORE_NAME> --name <ACCOUNT_NAME> 
```

```
$ safe-pm account --copy --store <STORE_NAME> --name <ACCOUNT_NAME> 
```

```
$ safe-pm account 
    --update \
    --store <STORE_NAME> \
    --name <ACCOUNT_NAME> \
    --password <PASSWORD TO USE>

or

$ safe-pm account 
    --update \
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
$ safe-pm account --delete --store <STORE_NAME> --name <ACCOUNT_NAME> 
```

```
$ safe-pm account --history --store <STORE_NAME> --name <ACCOUNT_NAME> 
```