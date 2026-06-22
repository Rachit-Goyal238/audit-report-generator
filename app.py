import streamlit as st
import tempfile
import os
import zipfile
import json
from main import generate_report

st.set_page_config(
    page_title="Audit Report Generator",
    layout="centered"
)

st.title("Audit Report Generator")

if "downloads" not in st.session_state:
    st.session_state.downloads = None

audit_id = st.text_input(
    "Enter Audit ID"
)

master_file = st.file_uploader(
    "Upload Master Excel",
    type=["xlsx"]
)

with open(
    "templates.json",
    "r",
    encoding="utf-8"
) as f:

    template_repository = json.load(f)

client = st.selectbox(
    "Select Client",
    list(
        template_repository.keys()
    )
)

template_type = st.selectbox(
    "Select Template",
    list(
        template_repository[
            client
        ].keys()
    )
)

report_pdf = st.file_uploader(
    "Upload Audit Report PDF",
    type=["pdf"]
)

annexure_pdf = st.file_uploader(
    "Upload Annexure PDF",
    type=["pdf"]
)

if st.button("Generate Report"):

    if not audit_id:

        st.error(
            "Please enter Audit ID"
        )

    elif not all([
        master_file,
        report_pdf,
        annexure_pdf
    ]):

        st.error(
            "Please upload all files"
        )

    else:

        try:

            with tempfile.TemporaryDirectory() as temp_dir:

                master_path = os.path.join(
                    temp_dir,
                    master_file.name
                )

                with open(master_path, "wb") as f:
                    f.write(
                        master_file.getbuffer()
                    )

                report_path = os.path.join(
                    temp_dir,
                    report_pdf.name
                )

                with open(report_path, "wb") as f:
                    f.write(
                        report_pdf.getbuffer()
                    )

                annexure_path = os.path.join(
                    temp_dir,
                    annexure_pdf.name
                )

                with open(annexure_path, "wb") as f:
                    f.write(
                        annexure_pdf.getbuffer()
                    )

                with st.spinner(
                    "Generating report..."
                ):

                    result = generate_report(
                        audit_id,
                        master_path,
                        client,
                        template_type,
                        report_path,
                        annexure_path
                    )

                zip_file = os.path.join(
                    tempfile.gettempdir(),
                    "Audit_Report_Package.zip"
                )

                with zipfile.ZipFile(
                    zip_file,
                    "w",
                    zipfile.ZIP_DEFLATED
                ) as zipf:

                    for file_path in [
                        result["excel"],
                        result["pdf"],
                        result["evidence"],
                        result["final"]
                    ]:

                        zipf.write(
                            file_path,
                            arcname=os.path.basename(
                                file_path
                            )
                        )

                with open(zip_file, "rb") as f:
                    zip_bytes = f.read()

                with open(result["excel"], "rb") as f:
                    excel_bytes = f.read()

                with open(result["evidence"], "rb") as f:
                    evidence_bytes = f.read()

                with open(result["final"], "rb") as f:
                    final_bytes = f.read()

                st.session_state.downloads = {
                    "zip": zip_bytes,
                    "excel": excel_bytes,
                    "evidence": evidence_bytes,
                    "final": final_bytes,
                    "excel_name": os.path.basename(
                        result["excel"]
                    ),
                    "evidence_name": os.path.basename(
                        result["evidence"]
                    ),
                    "final_name": os.path.basename(
                        result["final"]
                    )
                }


        except Exception as e:

            st.error(
                str(e)
            )

if st.session_state.downloads:

    downloads = st.session_state.downloads

    st.success(
        "Report generated successfully"
    )

    st.download_button(
        label="Download Complete Package (ZIP)",
        data=downloads["zip"],
        file_name="Audit_Report_Package.zip",
        mime="application/zip"
    )

    st.subheader(
        "Individual Downloads"
    )

    st.download_button(
        "Download Excel Report",
        data=downloads["excel"],
        file_name=downloads["excel_name"],
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        "Download Evidence PDF",
        data=downloads["evidence"],
        file_name=downloads["evidence_name"],
        mime="application/pdf"
    )

    st.download_button(
        "Download Final Report",
        data=downloads["final"],
        file_name=downloads["final_name"],
        mime="application/pdf"
    )