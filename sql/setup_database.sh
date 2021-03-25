#!/usr/bin/env bash

PGPASSWORD=postgres psql -d postgres -U postgres -f ./create_database.sql
PGPASSWORD=postgres psql -d shadowhawks -U postgres -f ./schema.sql
