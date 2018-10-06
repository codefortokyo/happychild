#!/bin/sh

cd /docker-entrypoint-initdb.d/

# import data
tar xzvf dataset.tar.gz
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/lines.csv' INTO TABLE lines  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/nurseries_scores.csv' INTO TABLE nurseries_scores  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/nurseries.csv' INTO TABLE nurseries  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/nursery_status.csv' INTO TABLE nursery_status  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
mysql -h localhost -u root happy_child -e "LOAD DATA LOCAL INFILE 'dataset/stations.csv' INTO TABLE stations  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES"
