import pandas as pd
import requests
import streamlit as st

st.set_page_config(layout="wide")


def process_invoices(files: list):
    """
    Sends the uploaded files to the API for processing and returns the response.
    """
    api_url = "http://127.0.0.1:8000/invoices/"
    headers = {"x-api-key": "supersecretapikey"}
    files_to_upload = [("files", (file.name, file, "application/pdf")) for file in files]

    response = requests.post(api_url, headers=headers, files=files_to_upload)
    if response.status_code == 200:
        return response.json()["invoices"]
    else:
        st.error(f"Failed to process invoices: {response.status_code} - {response.text}")
        return []


def main():
    st.title("Invoice Processor")

    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        if st.button("Process Invoices"):
            progress_bar = st.progress(0)
            with st.spinner("Processing..."):
                total_files = len(uploaded_files)
                processed_invoices = []

                for i, file in enumerate(uploaded_files):
                    invoices = process_invoices([file])
                    if invoices:
                        processed_invoices.extend(invoices)
                    progress_bar.progress((i + 1) / total_files)

                if processed_invoices:
                    df = pd.DataFrame(processed_invoices)
                    st.write("Processed Invoices")
                    st.dataframe(df, use_container_width=True)

                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="processed_invoices.csv",
                        mime="text/csv",
                    )


if __name__ == "__main__":
    main()

# streamlit run s_ui.py
