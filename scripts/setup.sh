#!/bin/bash

export DB_HOST=localhost
export DB_NAME=a12y
export DB_USER=admin
export DB_PASSWORD=F4kePlasticTrees!

# Create the database schema
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < create_database_schema.sql

# Exit with a success status
exit 0

