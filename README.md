# bq_fake_pii_table_creator

Library for creating BQ tables with fake pii data.

The drive and use case to create this library, was when you need a lot of data to validate if your org complies with regulations like
CCPA, HIPAA, GDPR.

[![PyPi][4]][5] [![License][6]][6] [![Issues][7]][8]

Usage from PyPi:
````bash
pip install bq-fake-pii-table-creator
bq-fake-pii-table-creator --help
````

<!--
  ⚠️ DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY ️️⚠️
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

## Table of Contents

<!-- toc -->

- [1. Environment setup](#1-environment-setup)
  * [1.1. Get the code](#11-get-the-code)
  * [1.2. Auth credentials](#12-auth-credentials)
      - [1.2.1. Create a service account and grant it below roles](#121-create-a-service-account-and-grant-it-below-roles)
      - [1.2.2. Download a JSON key and save it as](#122-download-a-json-key-and-save-it-as)
  * [1.3. Virtualenv](#13-virtualenv)
      - [1.3.1. Install Python 3.6+](#131-install-python-36)
      - [1.3.2. Create and activate a *virtualenv*](#132-create-and-activate-a-virtualenv)
      - [1.3.3. Install the dependencies](#133-install-the-dependencies)
      - [1.3.4. Set environment variables](#134-set-environment-variables)
  * [1.4. Docker](#14-docker)
- [2. Sample application entry point](#2-sample-application-entry-point)
  * [2.1. Run main.py](#21-run-mainpy)
  * [2.2. Or using Docker](#22-or-using-docker)

<!-- tocstop -->

-----

## 1. Environment setup

### 1.1. Get the code

````bash
git clone https://.../bq_fake_pii_table_creator.git
cd bq_fake_pii_table_creator
````

### 1.2. Auth credentials

##### 1.2.1. Create a service account and grant it below roles

The Service Account authenticated must have administrator privileges for Cloud Storage and BigQuery.

##### 1.2.2. Download a JSON key and save it as
- `<YOUR-CREDENTIALS_FILES_FOLDER>/bq_fake_pii_table_creator-credentials.json`

> Please notice this folder and file will be required in next steps.

### 1.3. Virtualenv

Using *virtualenv* is optional, but strongly recommended unless you use Docker or a PEX file.

##### 1.3.1. Install Python 3.6+

##### 1.3.2. Create and activate a *virtualenv*

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

##### 1.3.3. Install the dependencies

```bash
pip install --editable .
```

##### 1.3.4. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=credentials_file_path

```

### 1.4. Docker

See instructions below.

## 2. Sample application entry point

### 2.1. Run main.py

- Virtualenv

Only the project-id argument is required.

```bash
python main.py --project-id your_project --bq-dataset-name your_dataset --bq-table-name your_table --num-rows 5000 --num-cols 10 --obfuscate-col-names true
```


### 2.2. Or using Docker

```bash
docker build -t bq_fake_pii_table_creator .
docker run --rm --tty -v CREDENTIALS_FILES_FOLDER:/data \
bq_fake_pii_table_creator \
 --project-id your_project
```

[4]: https://img.shields.io/pypi/v/bq-fake-pii-table-creator.svg
[5]: https://pypi.org/project/bq-fake-pii-table-creator/
[6]: https://img.shields.io/github/license/mesmacosta/bq-fake-pii-table-creator.svg
[7]: https://img.shields.io/github/issues/mesmacosta/bq-fake-pii-table-creator.svg
[8]: https://github.com/mesmacosta/bq-fake-pii-table-creator/issues
