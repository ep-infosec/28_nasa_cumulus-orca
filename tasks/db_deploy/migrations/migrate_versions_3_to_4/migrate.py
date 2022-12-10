"""
Name: migrate.py

Description: Migrates the ORCA schema from version 3 to version 4.
"""
from typing import Dict

from orca_shared.database.shared_db import get_admin_connection, logger

import migrations.migrate_versions_3_to_4.migrate_sql as sql


def migrate_versions_3_to_4(config: Dict[str, str], is_latest_version: bool) -> None:
    """
    Performs the migration of the ORCA schema from version 3 to version 4 of
    the ORCA schema.
    Args:
        config (Dict): Connection information for the database.
        is_latest_version (bool): Flag to determine if version 4 is the latest schema version.
    Returns:
        None
    """
    # Get the admin engine to the app database
    admin_app_connection = get_admin_connection(config, config["user_database"])

    with admin_app_connection.connect() as connection:
        # Change to DBO role and set search path
        logger.debug("Changing to the dbo role to create objects ...")
        connection.execute(sql.text("SET ROLE orca_dbo;"))

        # Set the search path
        logger.debug("Setting search path to the ORCA schema to create objects ...")
        connection.execute(sql.text("SET search_path TO orca, public;"))

        # Create ORCA inventory tables
        # Create providers table
        logger.debug("Creating providers table ...")
        connection.execute(sql.providers_table_sql())
        logger.info("providers table created.")

        # Create collections table
        logger.debug("Creating collections table ...")
        connection.execute(sql.collections_table_sql())
        logger.info("collections table created.")

        # Create granules table
        logger.debug("Creating granules table ...")
        connection.execute(sql.granules_table_sql())
        logger.info("granules table created.")

        # Create files table
        logger.debug("Creating files table ...")
        connection.execute(sql.files_table_sql())
        logger.info("files table created.")

        # If v4 is the latest version, update the schema_versions table.
        if is_latest_version:
            logger.debug("Populating the schema_versions table with data ...")
            connection.execute(sql.schema_versions_data_sql())
            logger.info("Data added to the schema_versions table.")

        # Commit if there are no issues
        connection.commit()
