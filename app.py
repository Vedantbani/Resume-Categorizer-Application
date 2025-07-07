# import pandas as pd
# import pickle
# from pypdf import PdfReader
# import re
# import streamlit as st

# # Load models
# word_vector = pickle.load(open("tfidf.pkl", "rb"))
# model = pickle.load(open("model.pkl", "rb"))
# le = pickle.load(open("label_encoder.pkl", "rb"))

# def cleanResume(txt):
#     cleanText = re.sub(r'http\S+\s', ' ', txt)
#     cleanText = re.sub(r'RT|cc', ' ', cleanText)
#     cleanText = re.sub(r'#\S+\s', ' ', cleanText)
#     cleanText = re.sub(r'@\S+', '  ', cleanText)
#     cleanText = re.sub(r'[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
#     cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
#     cleanText = re.sub(r'\s+', ' ', cleanText)
#     return cleanText



# def categorize_resumes(uploaded_files):
#     results = []

#     for uploaded_file in uploaded_files:
#         if uploaded_file.name.endswith('.pdf'):
#             reader = PdfReader(uploaded_file)
#             page = reader.pages[0]
#             text = page.extract_text()
#             cleaned_resume = cleanResume(text)

#             input_features = word_vector.transform([cleaned_resume])

#             probabilities = model.predict_proba(input_features)[0]
#             top_indices = probabilities.argsort()[-3:][::-1]
#             top_categories = le.inverse_transform(top_indices)

#             results.append({
#                 'filename': uploaded_file.name,
#                 'Top 1': top_categories[0],
#                 'Top 2': top_categories[1],
#                 'Top 3': top_categories[2]
#             })

#     results_df = pd.DataFrame(results)
#     return results_df


# st.title("Resume Categorizer Application")
# st.subheader("With Python & Machine Learning")

# uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

# if st.button("Categorize Resumes"):
#     if uploaded_files:
#         results_df = categorize_resumes(uploaded_files)
#         st.write(results_df)
#         results_csv = results_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="Download results as CSV",
#             data=results_csv,
#             file_name='categorized_resumes.csv',
#             mime='text/csv',
#         )
#         st.success("Resumes categorization and processing completed.")
#     else:
#         st.error("Please upload files and specify the output directory.")


import pandas as pd
import pickle
from pypdf import PdfReader
import re
import streamlit as st

# Load models
word_vector = pickle.load(open("tfidf.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))

def cleanResume(txt):
    cleanText = re.sub(r'http\S+\s', ' ', txt)
    cleanText = re.sub(r'RT|cc', ' ', cleanText)
    cleanText = re.sub(r'#\S+\s', ' ', cleanText)
    cleanText = re.sub(r'@\S+', '  ', cleanText)
    cleanText = re.sub(r'[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText

def categorize_resumes(uploaded_files):
    results = []
    progress = st.progress(0)
    for i, uploaded_file in enumerate(uploaded_files):
        if uploaded_file.name.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            page = reader.pages[0]
            text = page.extract_text() or ""
            cleaned_resume = cleanResume(text)

            input_features = word_vector.transform([cleaned_resume])
            probabilities = model.predict_proba(input_features)[0]
            top_indices = probabilities.argsort()[-3:][::-1]
            top_categories = le.inverse_transform(top_indices)

            results.append({
                'File Name': uploaded_file.name,
                'Top 1 Category': top_categories[0],
                'Top 2 Category': top_categories[1],
                'Top 3 Category': top_categories[2]
            })

            progress.progress(int((i + 1) / len(uploaded_files) * 100))

    return pd.DataFrame(results)

# Streamlit page config
st.set_page_config(page_title="📂 Resume Categorizer", page_icon="📄", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to bottom right, #0f2027, #2c5364);
        background-size: cover;
        color: #f0f0f0;
    }
    .stButton>button {
        background-color: #f9a825;
        color: black;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
    }
    .stDownloadButton>button {
        background-color: #29b6f6;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
        border: none;
    }
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 10px;
        border-radius: 10px;
    }
    .stDataFrame {
        background-color: white;
        color: black;
        border-radius: 10px;
        padding: 5px;
    }
    hr {
        border: 1px solid #f9a825;
    }
    </style>
""", unsafe_allow_html=True)

# App content
st.markdown("""
    <h2 style='text-align: center;'>📄 Resume Categorizer Application</h2>
    <p style='text-align: center; color: #dddddd;'>Upload resumes in PDF format and let AI categorize them smartly.</p>
    <hr>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("📌 **Upload one or more resumes (PDF)**", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.info(f"✅ {len(uploaded_files)} file(s) selected. Ready to categorize!")

if st.button("🚀 Categorize Resumes"):
    if uploaded_files:
        results_df = categorize_resumes(uploaded_files)

        st.success("🎉 Resumes categorized successfully!")
        
        st.dataframe(results_df.style.set_properties(**{
            'background-color': '#f9f9f9',
            'color': 'black',
            'border-color': 'lightgray'
        }))
        
        results_csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇ Download results as CSV",
            data=results_csv,
            file_name='categorized_resumes.csv',
            mime='text/csv',
        )
    else:
        st.warning("⚠ Please upload at least one PDF file to categorize.")
