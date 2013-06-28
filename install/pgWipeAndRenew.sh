#!/bin/bash
#
dropdb flaskeval
createdb flaskeval
dropuser flaskeval
#createuser -SDRW flaskeval
psql -c "CREATE USER flaskeval WITH PASSWORD 'flaskeval';"


