#!/bin/tcsh

setenv ID `date '+%Y%m%d'`
pg_dump food | gzip -9 -c > /db_backups/foods.${ID}.sqldump.gz
aws s3 --region eu-central-1 cp /db_backups/foods.${ID}.sqldump.gz s3://fooddb-backup/

