
import pandas as pd
from sqlalchemy import create_engine, inspect
from app import app, db
from models import Clinic, User, Surgery, Technique, StayAdjustmentCriterion, Doctor, DischargeTimeSlot, StandardizedReason, Patient, Ticket, FpaModification

def export_db_to_excel():
    """
    Exports all tables from the SQLite database to a single Excel file,
    with each table in a separate sheet.
    """
    # IMPORTANT: This must run within the Flask application context
    # to have access to the db engine and models.
    with app.app_context():
        # Get the database URI from the Flask app configuration
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        engine = create_engine(db_uri)
        
        output_excel_path = 'database_view.xlsx'
        
        # A dictionary to hold DataFrames for each table
        tables_dfs = {}

        # List of all your model classes
        models = [
            Clinic, User, Surgery, Technique, StayAdjustmentCriterion, 
            Doctor, DischargeTimeSlot, StandardizedReason, Patient, 
            Ticket, FpaModification
        ]

        print("Starting database export...")

        for model in models:
            table_name = model.__tablename__
            try:
                # Read the entire table into a pandas DataFrame
                df = pd.read_sql_table(table_name, engine)
                tables_dfs[table_name] = df
                print(f"  - Successfully read table: {table_name} ({len(df)} rows)")
            except Exception as e:
                print(f"  - Error reading table {table_name}: {e}")

        if not tables_dfs:
            print("No data was read from the database. Aborting Excel export.")
            return

        # Write the DataFrames to an Excel file
        try:
            with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
                for table_name, df in tables_dfs.items():
                    df.to_excel(writer, sheet_name=table_name, index=False)
            print(f"\nSuccessfully exported all tables to '{output_excel_path}'")
        except Exception as e:
            print(f"\nError writing to Excel file: {e}")

def run_export():
    with app.app_context():
        export_db_to_excel()

if __name__ == '__main__':
    run_export()
