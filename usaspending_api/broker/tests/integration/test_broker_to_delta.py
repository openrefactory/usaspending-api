"""
Goal of test(s) in this module is to show
1. Populating delta tables from Broker DB tables
2. MERGEing in changed records from broker to that Delta table, detected e.g. by ``update_date`` or ``created_at` or
the like
"""
import psycopg2

from usaspending_api.common.helpers.sql_helpers import get_broker_dsn_string


# DONE: 1. add necessary fixtures that allow use of spark session, s3 unit test data bucket, unit test hive
#  metastore, broker DB connection
def test_broker_based_delta_table(
    spark, s3_unittest_data_bucket, hive_unittest_metastore_db, broker_server_dblink_setup
):
    source_broker_table = "sam_recipient"
    # DONE 2. Make sure broker DB can be connected
    # NOTE: Make sure you have a broker DB running, and have a DATA_BROKER_DATABASE_URL env var set that points to it
    with psycopg2.connect(dsn=get_broker_dsn_string()) as broker_connection:
        with broker_connection.cursor() as cursor:
            cursor.execute(
                f"select table_name from information_schema.tables where table_name = '{source_broker_table}'"
            )
            found_table = cursor.fetchone()[0]
            assert found_table == source_broker_table

    # TODO 3. Make sure empty source table (data_broker.public.sam_recipient) can be queried

    # TODO: 4. create test data in broker DB source table (see how Daniel did it with a json-based test data fixture
    #  in test_load_table_to_delta_for_broker_subaward

    # TODO: 5. Create target Delta table in delta lake (raw.sam_recipient, or maybe int.sam_recipient?)

    # TODO: 6. Make sure target Delta table can be fully reloaded, using the normal approach to load_table_to_delta,
    #          but from broker. See if Daniel was able to get this working with broker subaward

    # TODO: 7. (Could be another test) Create updates to broker data (one or more of insert, update, delete)

    # TODO: 8. Demonstrate a MERGE from source broker table to target delta table account for UPSERTs

    # TODO: 9. Demonstrate generating DELETEs from the target Delta table for source broker records that are gone
    #          using MERGE DELETE strategies
