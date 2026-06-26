import pandas as pd


def populate_rating(
    ws,
    base_data_file,
    agency_name
):

    df = pd.read_excel(
        base_data_file,
        sheet_name="Audited",
        keep_default_na=False
    )

    # Use Vendor Name from Column H only
    vendor_column = (
        df.iloc[:, 7]
        .astype(str)
        .str.strip()
    )

    df = df[
        vendor_column
        ==
        agency_name.strip()
    ]

    if len(df) == 0:

        raise Exception(
            f"No record found for agency '{agency_name}' in Audited sheet."
        )

    row = df.iloc[0]

    # -----------------------------
    # Populate Rating Header
    # -----------------------------

    # Vendor Name
    ws["C6"] = row.iloc[7]

    # Audit Date
    ws["C7"] = row.iloc[18]

    # CM Name
    ws["C8"] = row.iloc[23]

    # CM Employee ID
    ws["C9"] = row.iloc[22]

    # Agency Location
    ws["E6"] = row.iloc[20]

    # CCL Name (RCM)
    ws["E8"] = row.iloc[24]

    # Agency Discussion Person (Manager)
    ws["E10"] = row.iloc[15]

    # Agency Address
    ws["G6"] = row.iloc[11]

    # Auditor Name / Contact
    auditor = str(
        row.iloc[16]
    ).strip()

    contact = str(
        row.iloc[17]
    ).strip()

    ws["G8"] = (
        f"{auditor} / {contact}"
    )