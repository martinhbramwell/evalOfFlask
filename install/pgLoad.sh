#!/bin/bash
#
psql -c "insert into lease (official_id, official_name, nick_name, contract) values 
('3e3e', 'Barkersville N44-734', 'Barkers', 'Blabbity, blabbity, blah');" flaskeval
psql -c "insert into lease (official_id, official_name, nick_name, contract) values 
('8e4t', 'Janus D45-888', 'Janus', 'We hold these remarks to be self-contrad...');" flaskeval


