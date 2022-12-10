"""
Name: test_db_deploy.py

Description:  Unit tests for db_deploy.py.
"""
import os
import unittest
import uuid
from unittest.mock import MagicMock, patch

import db_deploy


class TestDbDeployFunctions(unittest.TestCase):
    """
    Tests the db_deploy functions.
    """

    @patch("db_deploy.get_configuration")
    @patch("db_deploy.task")
    @patch.dict(
        os.environ,
        {"DB_CONNECT_INFO_SECRET_ARN": "test"},
        clear=True,
    )
    def test_handler_happy_path(
        self, mock_task: MagicMock, mock_get_configuration: MagicMock
    ):
        """
        Does a happy path test. No real logic here as it just sets up the
        Cumulus Logger and the database configuration which are tested in
        other test cases. Only checks input is valid.
        """
        # Set values for the test
        # todo: Switch to randomized values generated per-test.
        event = {"orcaBuckets": ["orca_worm", "orca_versioned", "orca_special"]}
        config = {
            "admin_database": "admin_db",
            "admin_password": "admin123",
            "admin_username": "admin",
            "host": "aws.postgresrds.host",
            "port": 5432,
            "user_database": "user_db",
            "user_password": "user123",
            "user_username": "user",
        }
        mock_get_configuration.return_value = config

        # Run the function
        db_deploy.handler(event, {})

        # Check tests
        mock_task.assert_called_with(config, event["orcaBuckets"])

    @patch("db_deploy.get_configuration")
    @patch("db_deploy.task")
    @patch.dict(
        os.environ,
        {"DB_CONNECT_INFO_SECRET_ARN": "test"},
        clear=True,
    )
    def test_handler_bad_input(
        self, mock_task: MagicMock, mock_get_configuration: MagicMock
    ):
        """
        Tests handler and makes sure a failure occurs if the input is not correct.
        """
        # Set values for the test
        events = [
            {"orcaBuckets": []},
            {"orcaBuckets": 1234},
            {"orcaBuckets": "abcds"},
            {},
        ]
        config = {
            "admin_database": "admin_db",
            "admin_password": "admin123",
            "admin_username": "admin",
            "host": "aws.postgresrds.host",
            "port": 5432,
            "user_database": "user_db",
            "user_password": "user123",
            "user_username": "user",
        }
        mock_get_configuration.return_value = config

        # Run the function and see if it fails wit a value error
        for event in events:
            with self.subTest(event=event):
                with self.assertRaises(ValueError) as ve:
                    db_deploy.handler(event, {})

                value_error_message = str(ve.exception)
                self.assertEqual(
                    value_error_message,
                    "orcaBuckets must be a valid list of ORCA S3 bucket names.",
                )

    @patch("db_deploy.create_fresh_orca_install")
    @patch("db_deploy.create_database")
    @patch("db_deploy.get_admin_connection")
    @patch("db_deploy.app_db_exists")
    def test_task_no_database(
        self,
        mock_app_db_exists: MagicMock,
        mock_connection: MagicMock,
        mock_create_database: MagicMock,
        mock_create_fresh_orca_install: MagicMock,
    ):
        """
        Validates if the ORCA database does not exist, then it is created.
        """
        # Setup
        mock_app_db_exists.return_value = False
        config = {
            "admin_database": "admin_db",
            "admin_password": "admin123",
            "admin_username": "admin",
            "host": "aws.postgresrds.host",
            "port": 5432,
            "user_database": "user_db",
            "user_password": "user123",
            "user_username": "user",
        }
        orca_buckets = ["orca_worm", "orca_versioned", "orca_special"]

        # Call the task
        db_deploy.task(config, orca_buckets)

        # Check function calls
        mock_app_db_exists.assert_called_with(
            mock_connection().connect().__enter__(), config["user_database"]
        )
        mock_create_database.assert_called_once_with(config)
        mock_create_fresh_orca_install.assert_called_once_with(config, orca_buckets)

    @patch("db_deploy.get_admin_connection")
    @patch("db_deploy.create_fresh_orca_install")
    @patch("db_deploy.app_schema_exists")
    @patch("db_deploy.app_db_exists")
    def test_task_no_schema(
        self,
        mock_db_exists: MagicMock,
        mock_schema_exists: MagicMock,
        mock_fresh_install: MagicMock,
        mock_connection: MagicMock,
    ):
        """
        Validates that `create_fresh_orca_install` is called if no ORCA schema
        are present.
        """
        mock_db_exists.return_value = True
        mock_schema_exists.return_value = False
        config = {
            "admin_database": "admin_db",
            "admin_password": "admin123",
            "admin_username": "admin",
            "host": "aws.postgresrds.host",
            "port": 5432,
            "user_database": "user_db",
            "user_password": "user123",
            "user_username": "user",
        }
        orca_buckets = ["orca_worm", "orca_versioned", "orca_special"]

        db_deploy.task(config, orca_buckets)
        mock_fresh_install.assert_called_with(config, orca_buckets)

    @patch("db_deploy.get_admin_connection")
    @patch("db_deploy.perform_migration")
    @patch("db_deploy.get_migration_version")
    @patch("db_deploy.app_schema_exists")
    @patch("db_deploy.app_db_exists")
    def test_task_schmea_old_version(
        self,
        mock_db_exists: MagicMock,
        mock_schema_exists: MagicMock,
        mock_migration_version: MagicMock,
        mock_perform_migration: MagicMock,
        mock_connection: MagicMock,
    ):
        """
        Validates that `perform_migration` is called if the current schema
        version is older than the latest version.
        """
        mock_db_exists.return_value = True
        mock_schema_exists.return_value = True
        mock_migration_version.return_value = 1
        config = {
            "admin_database": "admin_db",
            "admin_password": "admin123",
            "admin_username": "admin",
            "host": "aws.postgresrds.host",
            "port": 5432,
            "user_database": "user_db",
            "user_password": "user123",
            "user_username": "user",
        }
        orca_buckets = ["orca_worm", "orca_versioned", "orca_special"]

        db_deploy.task(config, orca_buckets)
        mock_perform_migration.assert_called_with(1, config, orca_buckets)

    @patch("db_deploy.get_admin_connection")
    @patch("db_deploy.logger.info")
    @patch("db_deploy.get_migration_version")
    @patch("db_deploy.app_schema_exists")
    @patch("db_deploy.app_db_exists")
    def test_task_schema_current_version(
        self,
        mock_db_exists: MagicMock,
        mock_schema_exists: MagicMock,
        mock_migration_version: MagicMock,
        mock_logger_info: MagicMock,
        mock_connection: MagicMock,
    ):
        """
        validates that no action is taken if the current and latest versions
        are the same.
        """
        mock_db_exists.return_value = True
        mock_schema_exists.return_value = True
        mock_migration_version.return_value = db_deploy.LATEST_ORCA_SCHEMA_VERSION
        message = "Current ORCA schema version detected. No migration needed!"
        config = {
            "admin_database": "admin_db",
            "admin_password": "admin123",
            "admin_username": "admin",
            "host": "aws.postgresrds.host",
            "port": 5432,
            "user_database": "user_db",
            "user_password": "user123",
            "user_username": "user",
        }
        orca_buckets = ["orca_worm", "orca_versioned", "orca_special"]

        db_deploy.task(config, orca_buckets)
        mock_logger_info.assert_called_with(message)

    def test_app_db_exists_happy_path(self):
        """
        Does a happy path test for the function. No real logic to test.
        """
        # Create the mock connection object and the return value
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = [
            [
                True,
            ],
        ]

        # call the function
        db_exists = db_deploy.app_db_exists(mock_conn, uuid.uuid4().__str__())

        self.assertEqual(db_exists, True)

    def test_app_schema_exists_happy_path(self):
        """
        Does a happy path test for the function. No real logic to test.
        """
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = [
            [
                True,
            ],
        ]

        # call the function
        schema_exists = db_deploy.app_schema_exists(mock_conn)

        self.assertEqual(schema_exists, True)

    def test_app_versions_table_exists_happy_path(self):
        """
        Does a happy path test for the function. No real logic to test.
        """
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = [
            [
                True,
            ],
        ]

        # call the function
        table_exists = db_deploy.app_version_table_exists(mock_conn)

        self.assertEqual(table_exists, True)

    @patch("db_deploy.app_version_table_exists")
    def test_get_migration_version_happy_path(self, mock_table_exists):
        """
        Does a happy path test for the function. No real logic to test.
        """
        mock_conn = MagicMock()
        table_exists_array = [True, False]
        mock_conn.execute.return_value.fetchall.return_value = [
            [
                5,
            ],
        ]

        for table_exists in table_exists_array:
            with self.subTest(table_exists=table_exists):
                mock_table_exists.return_value = table_exists

                # call the function
                schema_version = db_deploy.get_migration_version(mock_conn)

                if table_exists:
                    self.assertEqual(schema_version, 5)
                else:
                    self.assertEqual(schema_version, 1)
