# Codeship cli

(Still In Dev)

Codeship client to help find text, see configurations by terminal

## Install

`pip install git+https://github.com/agutoli/codeship-cli.git --no-cache-dir --upgrade`

Note: This library is not published at pypi

## Configure

```shell
$ codeship configure
$ -> Codeship username: yourusername@corp.com
$ -> Codeship organization: YOUR-COMPANY-AT-CODESHIP
$ Saved at /Users/your_home/.codeship
```

## Commands

  * /search

    ```shell
    $ codeship search MY-SEARCH-TERM
    Codeship password: ****
    Searching...
    -> uuid=99999999-9999-9999-9999-999999999999: My_Company/some-project (26 occurrences)
    -> uuid=88888888-8888-8888-8888-888888888888: My_Company/other-project (51 occurrences)
    ```

  * /info

    ```shell
    $ codeship info 99999999-9999-9999-9999-999999999999
    Codeship password: ****
    Info project 99999999-9999-9999-9999-999999999999
    aes_key: null
    authentication_user: Walter White
    created_at: '2016-08-29T15:34:32.700Z'
    deployment_pipelines:
    - branch:
        branch_name: master
        match_mode: exact
      config:
        commands:
        - npm Install
        - ls -la
      position: 1
      ...
    ```
