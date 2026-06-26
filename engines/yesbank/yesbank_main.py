from openpyxl import load_workbook

from engines.yesbank.rating_utils import (
    populate_rating
)

from engines.yesbank.kaf_utils import (
    populate_kaf
)

from engines.yesbank.agency_utils import (
    populate_agency
)

from engines.yesbank.annexure_utils import (
    populate_annexure_1,
    populate_annexure_2
)


def generate_collection_report(
    base_data_file,
    kaf_file,
    annexure_file,
    template_file,
    output_file,
    agency_name
):

    wb = load_workbook(
        template_file
    )

    print(
        "Populating Rating..."
    )

    populate_rating(
        wb["Rating"],
        base_data_file,
        agency_name
    )

    print(
        "Populating KAF..."
    )

    populate_kaf(
        wb["KAF"],
        kaf_file,
        agency_name
    )

    print(
        "Populating Agency..."
    )

    populate_agency(
        wb["Agency"],
        wb["KAF"]
    )

    print(
        "Populating Annexure 1..."
    )

    populate_annexure_1(
        wb["Annexure 1"],
        annexure_file,
        agency_name
    )

    print(
        "Populating Annexure 2..."
    )

    populate_annexure_2(
        wb["Annexure 2"],
        annexure_file,
        agency_name
    )

    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    
    wb.save(
        output_file
    )

    print(
        "Collection report generated successfully."
    )