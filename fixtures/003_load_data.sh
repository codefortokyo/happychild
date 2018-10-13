#!/bin/sh

cd /docker-entrypoint-initdb.d/

# import data
tar xzvf dataset.tar.gz
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/nurseries.csv' INTO TABLE nurseries  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/nursery_free_nums.csv' INTO TABLE nursery_free_nums  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/stations.csv' INTO TABLE stations  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
