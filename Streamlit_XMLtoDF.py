import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st
from tkinter import Tk, filedialog

# Function to extract data from XML content and return a DataFrame
def extract_data_from_xml(xml_content):
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Namespace dictionary
    namespace = {'ns': 'http://www.emeter.com/energyip/amiinterface'}

    # Initialize lists to store extracted data
    reading_type_ids = []
    end_times = []
    values = []
    mrids = []

    # Iterate through the IntervalBlock elements
    for interval_block in root.findall(".//ns:IntervalBlock", namespace):
        reading_type_id = interval_block.find("ns:readingTypeId", namespace).text
        if reading_type_id == "1.0.1.8.0.255":
            end_time = interval_block.find(".//ns:IReading/ns:endTime", namespace).text
            value = interval_block.find(".//ns:IReading/ns:value", namespace).text
            mrid = root.find(".//ns:Meter/ns:mRID", namespace).text

            reading_type_ids.append(reading_type_id)
            end_times.append(end_time)
            values.append(value)
            mrids.append(mrid)

    # Create a DataFrame
    data = {
        "readingTypeId": reading_type_ids,
        "endTime": end_times,
        "value": values,
        "mRID": mrids
    }

    df = pd.DataFrame(data)
    return df

# Streamlit app
def main():
    st.title("XML Data Extraction and Export")

    # File uploader
    uploaded_files = st.file_uploader("Upload XML Files", type=["xml"], accept_multiple_files=True)

    # Process uploaded XML files
    dataframes = []
    for uploaded_file in uploaded_files:
        xml_content = uploaded_file.read()
        df = extract_data_from_xml(xml_content)
        dataframes.append(df)

    # Display extracted data on screen
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        st.write("Extracted DataFrame:")
        st.write(combined_df)

        # Export to Excel button
        if st.button("Export DataFrame to Excel"):
            export_file_path = st.text_input("Enter Excel file name:", "output.xlsx")
            combined_df.to_excel(export_file_path, index=False)
            st.success(f"DataFrame exported to {export_file_path}")
    else:
        st.write("No XML files uploaded.")

if __name__ == "__main__":
    main()
