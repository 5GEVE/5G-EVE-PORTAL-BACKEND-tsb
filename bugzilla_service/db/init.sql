-- Where the database scripts live
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "cube";
CREATE EXTENSION IF NOT EXISTS "earthdistance";

DROP TABLE IF EXISTS bzuser;

CREATE TABLE bzuser (
    _id 			  uuid DEFAULT uuid_generate_v4 (),
    email 		      VARCHAR NOT NULL,
    password          VARCHAR NOT NULL,
    full_name         VARCHAR,
    apikey            VARCHAR,
    PRIMARY KEY(_id)
);
