DROP SCHEMA IF EXISTS dr CASCADE;
DROP ROLE IF EXISTS druser;
REVOKE CONNECT ON DATABASE orca FROM dbo;
DROP USER IF EXISTS dbo;
REVOKE CREATE ON DATABASE orca FROM GROUP drdbo_role;
REVOKE CONNECT ON DATABASE orca FROM GROUP drdbo_role;
DROP GROUP IF EXISTS drdbo_role;
REVOKE CONNECT ON DATABASE orca FROM GROUP dr_role;
DROP GROUP IF EXISTS dr_role;
COMMIT;
