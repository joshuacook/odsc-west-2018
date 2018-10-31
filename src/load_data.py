from lib.database import query_database, query_to_dataframe
from psycopg2 import ProgrammingError

if __name__ == "__main__":
    pre_etl_adult_df = query_to_dataframe("""
        SELECT
            age,
            capital_gain,
            capital_loss,
            education,
            gender,
            hours_per_week,
            income_label,
            marital_status,
            native_country,
            occupation,
            race,
            relationship,
            workclass
        FROM adult
        WHERE (
            (native_country != ' ?') AND
            (occupation != ' ?') AND
            (workclass != ' ?')
        );
    """)

    pre_etl_adult_df["income_label"] = (pre_etl_adult_df["income_label"] == " >50K").astype(int)
    pre_etl_adult_df["gender"] = (pre_etl_adult_df["gender"] == " Female").astype(int)

    try:
        query_database("""
        BEGIN;
        DROP TABLE adult_for_modeling;
        COMMIT;
        """)
    except ProgrammingError as e:
        print(e)

    query_database("""
        BEGIN;
        CREATE TABLE adult_for_modeling (
            age INTEGER,
            capital_gain INTEGER,
            capital_loss INTEGER,
            education TEXT,
            gender INTEGER,
            hours_per_week INTEGER,
            income_label INTEGER,
            marital_status TEXT,
            native_country TEXT,
            occupation TEXT,
            race TEXT,
            relationship TEXT,
            workclass TEXT
        );
        COMMIT;
        """, fetch_res=False)
    print("adult_for_modeling table created")

    query_database(f"""
    BEGIN;
    INSERT INTO adult_for_modeling (
        age,
        capital_gain,
        capital_loss,
        education,
        gender,
        hours_per_week,
        income_label,
        marital_status,
        native_country,
        occupation,
        race,
        relationship,
        workclass
    )
    VALUES {','.join(str(record) for record in pre_etl_adult_df.to_records(index=False))};
    COMMIT;
    """, fetch_res=False)
