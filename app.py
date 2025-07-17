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
#     progress = st.progress(0)
#     for i, uploaded_file in enumerate(uploaded_files):
#         if uploaded_file.name.endswith('.pdf'):
#             reader = PdfReader(uploaded_file)
#             page = reader.pages[0]
#             text = page.extract_text() or ""
#             cleaned_resume = cleanResume(text)

#             input_features = word_vector.transform([cleaned_resume])
#             probabilities = model.predict_proba(input_features)[0]
#             top_indices = probabilities.argsort()[-3:][::-1]
#             top_categories = le.inverse_transform(top_indices)

#             results.append({
#                 'File Name': uploaded_file.name,
#                 'Top 1 Category': top_categories[0],
#                 'Top 2 Category': top_categories[1],
#                 'Top 3 Category': top_categories[2]
#             })

#             progress.progress(int((i + 1) / len(uploaded_files) * 100))

#     return pd.DataFrame(results)

# # Streamlit page config
# st.set_page_config(page_title="📂 Resume Categorizer", page_icon="📄", layout="wide")

# # Custom CSS for styling
# st.markdown("""
#     <style>
#     .stApp {
#         background-image: linear-gradient(to bottom right, #0f2027, #2c5364);
#         background-size: cover;
#         color: #f0f0f0;
#     }
#     .stButton>button {
#         background-color: #f9a825;
#         color: black;
#         border-radius: 8px;
#         padding: 10px 20px;
#         font-size: 16px;
#         border: none;
#     }
#     .stDownloadButton>button {
#         background-color: #29b6f6;
#         color: white;
#         border-radius: 8px;
#         padding: 8px 16px;
#         font-size: 14px;
#         border: none;
#     }
#     .stFileUploader {
#         background-color: rgba(255, 255, 255, 0.85);
#         padding: 10px;
#         border-radius: 10px;
#     }
#     .stDataFrame {
#         background-color: white;
#         color: black;
#         border-radius: 10px;
#         padding: 5px;
#     }
#     hr {
#         border: 1px solid #f9a825;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # App content
# st.markdown("""
#     <h2 style='text-align: center;'>📄 Resume Categorizer Application</h2>
#     <p style='text-align: center; color: #dddddd;'>Upload resumes in PDF format and let AI categorize them smartly.</p>
#     <hr>
# """, unsafe_allow_html=True)

# uploaded_files = st.file_uploader("📌 **Upload one or more resumes (PDF)**", type="pdf", accept_multiple_files=True)

# if uploaded_files:
#     st.info(f"✅ {len(uploaded_files)} file(s) selected. Ready to categorize!")

# if st.button("🚀 Categorize Resumes"):
#     if uploaded_files:
#         results_df = categorize_resumes(uploaded_files)

#         st.success("🎉 Resumes categorized successfully!")
        
#         st.dataframe(results_df.style.set_properties(**{
#             'background-color': '#f9f9f9',
#             'color': 'black',
#             'border-color': 'lightgray'
#         }))
        
#         results_csv = results_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="⬇ Download results as CSV",
#             data=results_csv,
#             file_name='categorized_resumes.csv',
#             mime='text/csv',
#         )
#     else:
#         st.warning("⚠ Please upload at least one PDF file to categorize.")



import pandas as pd
import pickle
from pypdf import PdfReader
import re
import streamlit as st

# Load models
word_vector = pickle.load(open("tfidf.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))

# Load Job Role Details Dataset
job_details_df = pd.read_csv("IT_Job_Details_Dataset.csv")

# Clean Resume Function
def cleanResume(txt):
    cleanText = re.sub(r'http\S+\s', ' ', txt)
    cleanText = re.sub(r'RT|cc', ' ', cleanText)
    cleanText = re.sub(r'#\S+\s', ' ', cleanText)
    cleanText = re.sub(r'@\S+', '  ', cleanText)
    cleanText = re.sub(r'[%s]' % re.escape(r"""!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText

# Fetch Job Details from IT Dataset
def get_job_details(job_role, min_salary, industry):
    filtered = job_details_df[job_details_df['Job Role'].str.lower() == job_role.lower()]
    if min_salary:
        filtered = filtered[filtered['Salary Estimate'].str.extract(r'(\d+)').astype(float)[0] >= min_salary]
    if industry and industry != "All":
        filtered = filtered[filtered['Industry'].str.contains(industry, case=False)]
    if not filtered.empty:
        return filtered.iloc[0].to_dict()
    return None

# Categorize resumes into top 3 roles
def categorize_resumes_top3(uploaded_files):
    categorized_results = []
    progress = st.progress(0)

    for i, uploaded_file in enumerate(uploaded_files):
        reader = PdfReader(uploaded_file)
        text = reader.pages[0].extract_text() or ""
        cleaned_resume = cleanResume(text)

        input_features = word_vector.transform([cleaned_resume])
        probabilities = model.predict_proba(input_features)[0]
        top_indices = probabilities.argsort()[-3:][::-1]
        top_roles = le.inverse_transform(top_indices)

        result = {
            'File Name': uploaded_file.name,
            'Top 1 Role': top_roles[0],
            'Top 2 Role': top_roles[1],
            'Top 3 Role': top_roles[2]
        }

        categorized_results.append(result)
        progress.progress(int((i + 1) / len(uploaded_files) * 100))

    return pd.DataFrame(categorized_results)

# Predict job details for top 3 roles
def predict_jobs_top3(categorized_df, min_salary, industry):
    final_results = []
    for _, row in categorized_df.iterrows():
        for role in [row['Top 1 Role'], row['Top 2 Role'], row['Top 3 Role']]:
            job_info = get_job_details(role, min_salary, industry)
            if job_info:
                result = {
                    'File Name': row['File Name'],
                    'Predicted Role': role,
                    'Skills Required': job_info['Skills Required'],
                    'Salary Estimate': job_info['Salary Estimate'],
                    'Top Companies': job_info['Top Companies'],
                    'Industry': job_info['Industry'],
                    'Growth Path': job_info['Growth Path']
                }
                final_results.append(result)
    return pd.DataFrame(final_results)

# Streamlit Page Setup
st.set_page_config(page_title="📂 Resume Categorizer & Job Recommender", page_icon="📄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(to bottom right, #ffffff, #d9e4f5);
    background-size: cover;
    color: #1f1f1f;
}

.stTitle h1 {
    font-weight: 700;
    font-size: 50px;
    color: #1f4e79;
}

.stMarkdown p {
    font-size: 18px;
    color: #1f1f1f;
}

.stFileUploader, .stDataFrame, .stNumberInput, .stSelectbox, .stExpander {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 15px;
    padding: 15px;
    font-size: 18px;
    color: #1f1f1f;
}

.stButton>button, .stDownloadButton>button {
    background: linear-gradient(to right, #1f4e79, #5591c9);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 12px 25px;
    font-size: 18px;
}

.stButton>button:hover, .stDownloadButton>button:hover {
    background: linear-gradient(to right, #4f93ce, #71b7f5);
}

hr {
    border: 2px solid #1f4e79;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 Resume Categorizer & IT Job Predictor")
st.markdown("Upload resumes, categorize them, apply filters, and see detailed job recommendations.")

uploaded_files = st.file_uploader("📌 Upload one or more resumes (PDF)", type="pdf", accept_multiple_files=True)

min_salary = st.number_input("💰 Minimum Salary (LPA)", min_value=0, value=0)
industries = ["All"] + sorted(job_details_df['Industry'].dropna().unique().tolist())
industry = st.selectbox("🏭 Filter by Industry", industries)

if uploaded_files and st.button("🚀 Categorize Resumes"):
    categorized_df = categorize_resumes_top3(uploaded_files)
    st.session_state['categorized_df'] = categorized_df
    st.session_state['show_prediction'] = False
    st.success("✅ Categorization done!")
    st.dataframe(categorized_df)

if 'categorized_df' in st.session_state:
    if st.button("🔍 Predict Filtered Job Details"):
        predicted_df = predict_jobs_top3(st.session_state['categorized_df'], min_salary, industry)
        st.session_state['predicted_df'] = predicted_df
        st.session_state['show_prediction'] = True

if st.session_state.get('show_prediction'):
    predicted_df = st.session_state.get('predicted_df')
    if predicted_df is not None:
        for _, row in predicted_df.iterrows():
            with st.expander(f"📌 {row['File Name']} → {row['Predicted Role']}"):
                st.write(f"**Skills Required:** {row['Skills Required']}")
                st.write(f"**Salary Estimate:** {row['Salary Estimate']}")
                st.write(f"**Industry:** {row['Industry']}")
                st.write(f"**Growth Path:** {row['Growth Path']}")
                companies = row['Top Companies'].split(', ')
                st.write("**Top Companies:**")
                for company in companies:
                    st.write(f"- {company}")
        csv = predicted_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download All Job Details as CSV", csv, "jobs.csv", "text/csv")
