#!/usr/bin/env bash

PGPASSWORD=postgres psql -d postgres -U postgres -f ./create_database.sql
PGPASSWORD=hawk psql -d shadowhawks -U hawk -f ./schema.sql
