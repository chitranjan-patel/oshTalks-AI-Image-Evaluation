<div align="center">
  <h1>🌟 Josh Talks AI: Text-to-Image Evaluation 🌟</h1>
  <p><i>Blind A/B/C human evaluation of state-of-the-art AI models for Indian Fashion E-commerce</i></p>

  <a href="https://oshtalks-ai-image-evaluation-qgwypxynawjsdgutzcuq9z.streamlit.app/">
    <img src="https://img.shields.io/badge/🔴_Live_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Live App">
  </a>
  <a href="https://github.com/chitranjan-patel/oshTalks-AI-Image-Evaluation">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</div>

<hr>

## 🚀 Overview

This project evaluates the performance of cutting-edge Text-to-Image AI models specifically tailored for the **Indian context**, focusing on the **Indian Fashion E-commerce** use case. To ensure unbiased results, the application utilizes a **Blind A/B/C Evaluation** method where participants rate randomized AI-generated images without knowing the underlying models.

### 🤖 Models Evaluated
1. **OpenAI GPT Image 1 (DALL·E)**
2. **Google Gemini 2.5 Flash Image**
3. **Google Gemini 3.1 Flash Image Preview**

---

## 🛠️ Tech Stack & Workflow

- **Frontend & App Logic:** [Streamlit](https://streamlit.io/) (Python)
- **Database & Storage:** Google Sheets API (`st-gsheets-connection`)
- **Data Analysis & Visualization:** Pandas, Matplotlib, Altair
- **Deployment:** Streamlit Community Cloud

### 🔄 Data Workflow
1. **Participant View:** Users evaluate 3 randomized, anonymized images.
2. **Evaluation:** Rating on a 1-5 scale across 5 distinct dimensions (Prompt Adherence, Visual Quality, Realism, Indian Contextual Fit, E-commerce Usefulness).
3. **Storage:** Responses are instantly and securely written to a private Google Sheet.
4. **Admin Dashboard:** Admins can view the real mapping (which model generated which image) and access the raw evaluation data.

---

## 💻 Running on Localhost

Want to run this project on your own machine? Follow these simple steps:

### 1. Clone the Repository
```bash
git clone https://github.com/chitranjan-patel/oshTalks-AI-Image-Evaluation.git
cd oshTalks-AI-Image-Evaluation
```

### 2. Install Dependencies
Make sure you have Python 3.9+ installed.
```bash
pip install -r requirements.txt
```

### 3. Setup Secrets (Google Sheets Configuration)
To enable the database connection locally:
1. Create a `.streamlit/` folder in the project root.
2. Copy `.streamlit/secrets.toml.example` and rename it to `secrets.toml`.
3. Add your Google Service Account JSON credentials inside `secrets.toml`.

### 4. Run the App
```bash
python -m streamlit run app.py
```
> The app will automatically open in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```text
JoshTalksAI_TextToImage_Evaluation/
├── 01_Prompts/                # Master prompts used for generation
├── 02_Generated_Images/       # Raw AI-generated images
├── 03_Participant_Ratings/    # Consent forms and CSV structure
├── 04_Screenshots/            # UI and generation proofs
├── 05_Analysis/               # Final analysis & charts
├── 06_Dashboard/              # Dashboard components
├── 07_Main_Report/            # Comprehensive evaluation report
├── 08_One_Page_Report/        # Executive summary
├── 09_Video/                  # Presentation video script
├── 10_Metadata/               # Setup instructions & image metadata
├── app.py                     # Main Streamlit Application
└── requirements.txt           # Python dependencies
```

---

<div align="center">
  <i>Built with ❤️ for Josh Talks AI Evaluation Assignment</i>
</div>
