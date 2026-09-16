import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime
import matplotlib.pyplot as plt
from streamlit_gsheets import GSheetsConnection
import altair as alt

st.set_page_config(page_title="India Text-to-Image Evaluation", layout="wide", page_icon="🎨")

# Custom CSS
st.markdown("""
<style>
    /* Reduce top padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        border-color: #45a049;
    }
    div[data-testid="stImage"] img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = "03_Participant_Ratings/rating_data.csv"
IMAGE_DIR = "02_Generated_Images"
MODELS = ["GPT Image 1", "Gemini 2.5 Flash Image", "Gemini 3.1 Flash Image Preview"]
MODEL_DIRS = {
    "GPT Image 1": "GPT_Image_1",
    "Gemini 2.5 Flash Image": "Gemini_2.5_Flash_Image",
    "Gemini 3.1 Flash Image Preview": "Gemini_3.1_Flash_Image_Preview"
}

SHEET_URL = "https://docs.google.com/spreadsheets/d/11Q4AB7_vtApnDRT9Ap2RL611XBaGqdVxDLUyG8Px1_o/edit?gid=0#gid=0"

def get_connection():
    try:
        if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
            return st.connection("gsheets", type=GSheetsConnection)
    except Exception:
        pass
    return None

def load_data():
    conn = get_connection()
    if conn is not None:
        try:
            df = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
            df = df.dropna(how='all')
            if not df.empty:
                return df
        except Exception:
            pass
            
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
            if not df.empty:
                return df
        except Exception:
            pass
    return pd.DataFrame()

def save_data(new_row):
    df = load_data()
    
    if not df.empty and 'email' in df.columns:
        existing_emails = [str(e).strip().lower() for e in df['email'].values if pd.notnull(e)]
        if new_row['email'].strip().lower() in existing_emails:
            raise ValueError("An evaluation from this email has already been submitted.")
            
    new_df = pd.DataFrame([new_row])
    updated_df = pd.concat([df, new_df], ignore_index=True)
    
    conn = get_connection()
    if conn is not None:
        try:
            conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=updated_df)
            return
        except Exception as e:
            st.error(f"Failed to save to Google Sheets: {e}")
            
    updated_df.to_csv(DATA_PATH, index=False)

def get_images():
    images = {}
    for model, folder in MODEL_DIRS.items():
        path = os.path.join(IMAGE_DIR, folder)
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            if files:
                images[model] = os.path.join(path, files[0])
            else:
                images[model] = None
        else:
            images[model] = None
    return images

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Participant Evaluation", "Admin Dashboard", "Image Comparison"])

if page == "Participant Evaluation":
    st.title("🎨 India Text-to-Image Evaluation")
    st.subheader("Indian Fashion E-commerce — Human Evaluation")
    
    images = get_images()
    missing_images = [m for m, p in images.items() if p is None]
    
    if missing_images:
        st.warning(f"Waiting for images to be generated for: {', '.join(missing_images)}. Please run the evaluation later.")
    else:
        if get_connection() is None:
            st.warning("⚠️ **Warning:** Google Sheets connection secrets not found. Running in local fallback mode. Submissions will be saved to local CSV, which will **NOT** persist on Streamlit Cloud. Do not use for real participants in production.")
            
        st.write("Please fill out the form below to begin the evaluation.")
        
        with st.form("participant_form"):
            st.markdown("### Participant Information")
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            with col2:
                email = st.text_input("Email Address", placeholder="rahul@example.com")
            with col3:
                age = st.number_input("Age", min_value=1, max_value=120, step=1, value=18)
                
            consent = st.checkbox("I confirm that I am 18 years or older. I voluntarily participated in this evaluation. I consent to my name, email, and responses/ratings being included in this assignment submission for hiring evaluation purposes.")
            
            st.divider()
            
            st.markdown("### Image Evaluation")
            st.write("Please rate the following images (Image A, Image B, Image C) on a scale of 1 to 5.")
            st.info("**Scale:** 1 = Very Poor | 2 = Poor | 3 = Average | 4 = Good | 5 = Excellent")
            
            # Randomize images
            if 'image_order' not in st.session_state:
                shuffled_models = list(MODELS)
                random.shuffle(shuffled_models)
                st.session_state.image_order = shuffled_models
            
            order = st.session_state.image_order
            labels = ["Image A", "Image B", "Image C"]
            
            ratings = {}
            
            # Show images and sliders side-by-side
            img_cols = st.columns(3)
            
            for i, label in enumerate(labels):
                with img_cols[i]:
                    st.markdown(f"#### {label}")
                    model_name = order[i]
                    img_path = images[model_name]
                    st.image(img_path, use_container_width=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True) # spacer
                    
                    ratings[label] = {
                        'model': model_name,
                        'prompt_adherence': st.slider("Prompt Adherence", 1, 5, 3, key=f"{label}_pa"),
                        'visual_quality': st.slider("Visual Quality", 1, 5, 3, key=f"{label}_vq"),
                        'realism': st.slider("Realism", 1, 5, 3, key=f"{label}_re"),
                        'indian_fit': st.slider("Indian Contextual Fit", 1, 5, 3, key=f"{label}_if"),
                        'ecommerce_usefulness': st.slider("E-commerce Usefulness", 1, 5, 3, key=f"{label}_eu")
                    }
            
            st.divider()
            st.markdown("### Final Decision")
            overall_choice = st.radio("Which image would you choose overall for an Indian fashion e-commerce campaign?", labels, horizontal=True)
            reason = st.text_area("Why did you choose this image? (Optional)", placeholder="E.g., The lighting looks more natural...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Submit Evaluation 🚀")
            
            if submitted:
                if not consent:
                    st.error("You must provide consent to submit the evaluation.")
                elif not name or not email:
                    st.error("Please provide your name and email.")
                elif age < 18:
                    st.error("You must be 18 or older to participate.")
                else:
                    new_row = {
                        "participant_id": f"P_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "name": name,
                        "email": email,
                        "age": age,
                        "consent": consent,
                        "image_order": ",".join(order),
                        "overall_choice": ratings[overall_choice]['model'],
                        "reason": reason,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    for i, label in enumerate(labels):
                        prefix = ["image_a", "image_b", "image_c"][i]
                        r = ratings[label]
                        new_row[f"{prefix}_model"] = r['model']
                        new_row[f"{prefix}_prompt_adherence"] = r['prompt_adherence']
                        new_row[f"{prefix}_visual_quality"] = r['visual_quality']
                        new_row[f"{prefix}_realism"] = r['realism']
                        new_row[f"{prefix}_indian_fit"] = r['indian_fit']
                        new_row[f"{prefix}_ecommerce_usefulness"] = r['ecommerce_usefulness']
                        
                    try:
                        save_data(new_row)
                        st.balloons()
                        st.success("🎉 Thank you for your submission! Your feedback has been recorded.")
                        del st.session_state.image_order
                    except ValueError as e:
                        st.error(str(e))

elif page == "Admin Dashboard":
    st.title("📊 Admin Dashboard: Results & Leaderboard")
    st.markdown("Monitor human evaluation scores and preferences.")
    
    df = load_data()
    
    if df.empty:
        st.info("Awaiting participant data. No evaluations have been submitted yet.")
    else:
        # High level metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Participants", len(df))
        
        # Calculate scores
        results = []
        for model in MODELS:
            model_data = []
            for prefix in ['image_a', 'image_b', 'image_c']:
                subset = df[df[f'{prefix}_model'] == model]
                if not subset.empty:
                    cols = [c for c in subset.columns if c.startswith(prefix) and c != f'{prefix}_model']
                    model_data.append(subset[cols].rename(columns=lambda x: x.replace(f"{prefix}_", "")))
            
            if model_data:
                combined = pd.concat(model_data)
                avg_scores = combined.mean()
                overall = avg_scores.mean()
                
                pref_count = len(df[df['overall_choice'] == model])
                pref_pct = (pref_count / len(df)) * 100
                
                results.append({
                    "Model": model,
                    "Overall Score": round(overall, 2),
                    "Prompt Adherence": round(avg_scores.get('prompt_adherence', 0), 2),
                    "Visual Quality": round(avg_scores.get('visual_quality', 0), 2),
                    "Realism": round(avg_scores.get('realism', 0), 2),
                    "Indian Contextual Fit": round(avg_scores.get('indian_fit', 0), 2),
                    "E-commerce Usefulness": round(avg_scores.get('ecommerce_usefulness', 0), 2),
                    "Human Preference (%)": round(pref_pct, 2)
                })
        
        if results:
            results_df = pd.DataFrame(results).sort_values(by="Overall Score", ascending=False)
            results_df.insert(0, "Rank", range(1, len(results_df) + 1))
            
            top_model = results_df.iloc[0]['Model']
            top_pref = results_df.sort_values(by="Human Preference (%)", ascending=False).iloc[0]['Model']
            
            col2.metric("Highest Rated Model", top_model)
            col3.metric("Most Preferred Model", top_pref)
            
            st.divider()
            
            st.subheader("🏆 Leaderboard")
            st.dataframe(results_df.style.highlight_max(axis=0, subset=["Overall Score", "Human Preference (%)"], color='#4CAF50'), use_container_width=True)
            
            st.divider()
            st.subheader("📈 Analytics")
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown("**Overall Scores by Model**")
                bar_chart = alt.Chart(results_df).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                    x=alt.X('Model', sort='-y'),
                    y='Overall Score',
                    color=alt.Color('Model', scale=alt.Scale(scheme='category10')),
                    tooltip=['Model', 'Overall Score']
                ).properties(height=350)
                st.altair_chart(bar_chart, use_container_width=True)
            
            with chart_col2:
                st.markdown("**Human Preference (%)**")
                pie_chart = alt.Chart(results_df).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="Human Preference (%)", type="quantitative"),
                    color=alt.Color(field="Model", type="nominal"),
                    tooltip=['Model', 'Human Preference (%)']
                ).properties(height=350)
                st.altair_chart(pie_chart, use_container_width=True)

elif page == "Image Comparison":
    st.title("🔍 Image Comparison Screen")
    st.markdown("Compare the raw outputs from the models side by side.")
    
    with st.expander("View Master Prompt"):
        with open("01_Prompts/master_prompt.md", "r") as f:
            prompt_text = f.read()
        st.info(f"{prompt_text}")
    
    images = get_images()
    
    cols = st.columns(3)
    for i, model in enumerate(MODELS):
        with cols[i]:
            st.markdown(f"**{model}**")
            if images[model]:
                st.image(images[model], use_container_width=True)
            else:
                st.error("Image not generated yet.")
