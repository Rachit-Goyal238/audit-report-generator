import pandas as pd

from engines.yesbank.yesbank_main import (
    generate_collection_report
)


BASE_DATA_FILE = "Base_Data.xlsx"
KAF_FILE = "KAF.xlsx"
ANNEXURE_FILE = "Annexure.xlsx"

TEMPLATE_FILE = (
    "templates/YesBank/YesBank_Collection_Template_2026-27.xlsx"
)

OUTPUT_FILE = (
    "test_yesbank_output.xlsx"
)

print(
    "Annexure Sheets:"
)

print(
    pd.ExcelFile(
        ANNEXURE_FILE
    ).sheet_names
)

print(
    "\nKAF Sheets:"
)

print(
    pd.ExcelFile(
        KAF_FILE
    ).sheet_names
)

print(
    "\nBase Data Sheets:"
)

print(
    pd.ExcelFile(
        BASE_DATA_FILE
    ).sheet_names
)

agency_name = input(
    "\nEnter Agency Name: "
).strip()

generate_collection_report(
    base_data_file=BASE_DATA_FILE,
    kaf_file=KAF_FILE,
    annexure_file=ANNEXURE_FILE,
    template_file=TEMPLATE_FILE,
    output_file=OUTPUT_FILE,
    agency_name=agency_name
)

print(
    "\n===================================="
)

print(
    "YESBANK COLLECTION TEST COMPLETED"
)

print(
    f"Agency : {agency_name}"
)

print(
    f"Output : {OUTPUT_FILE}"
)

print(
    "===================================="
)