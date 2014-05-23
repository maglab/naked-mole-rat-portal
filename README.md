The Naked Mole-rat Genome Portal
================================

A genome portal designed for the Naked Mole Rat Genome. It supports the searching and display of a genome, including linked genes. It also provides the jBrowse genome viewer for a more detailed look at the structure of the gene in the details pages. 

Please be aware as this portal was not deigned for portability or for generalised use there may be issues when running it with other genomes and documentation is lacking in most areas.

## Requirements

**Python:**
- Django 1.5 or higher
- South
- Biopytho
- django-haystack 2.1 or higher
- django-tables2
- ecdsa
- elasticsearch 1.0 or higher
- psycopg2
- pycrypto
- pyelasticsearch 0.6.1 or higher
- pyjade 2.0 or higher
- python-ptrace
- requests
- simplejson
- six
- sqlparse
- urllib3
- wsgiref

**Other:**
- PostgreSQL 9.1 or higher
- Elasticsearch 1.2 or higher

## Setting up

This portal has been designed to run using Nginx and a uwsgi server such as uwsgi. See Django documentation for how to run a Django instance. 

## Loading data

The portal provides a way of importing data in through an admin command. The basic syntax is `manage.py load_data <data type> <files>`.

## Customisation

You will have to customise the templates directly to change the content as most is static. LESS files are provided to make it easier to change the colour scheme.
