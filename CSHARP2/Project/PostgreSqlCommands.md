# Commands I run setting up the project.

Creating the database and user that has access to it.

```sql
CREATE DATABASE coworking_db;
CREATE USER coworking_user WITH PASSWORD 'yourpassword';
ALTER ROLE coworking_user SET client_encoding TO 'utf8';
ALTER ROLE coworking_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE coworking_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE coworking_db TO coworking_user;
```

I also had to change the `/var/lib/pgsql/data/pg_hba.conf` file
in order to pass the password in the `appsettings.json` as plain
text and for the postgres to do md5 hashing for me. 

WARN: In production code this should not be handled like this.

```conf
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5

# Local connections:
local   all             all                                     md5

# IPv6 local connections:
host    all             all             ::1/128                 md5
```




