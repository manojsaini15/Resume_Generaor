# AI Resume Builder

An AI-powered Streamlit application that turns your profile information into a professional, ATS-friendly resume. It uses Mistral AI through LangChain to create a clean **plain-text** resume and lets you download the result as a `.txt` file.

> **Current output format:** plain text (`.txt`). This project does not generate DOCX or PDF files.

## Features

- Simple web interface built with Streamlit
- Collects key candidate details, including contact information, professional summary, skills, education, experience, projects, and certifications
- Uses Mistral AI to organize the supplied information into a professional resume
- Prompts the model to produce clear, ATS-friendly plain text
- Lets you choose from the Mistral model options exposed in the app
- Displays the generated resume in the browser
- Downloads the generated resume as a `.txt` file

## Tech Stack

- **Python**
- **Streamlit** for the user interface
- **LangChain** for prompt and model orchestration
- **Mistral AI** for resume generation
- **python-dotenv** for loading local environment variables

## Project Structure

```text
AI-Resume-Builder/
├── resumegenerator_ui.py       # Streamlit app variant
├── resumegenerator_ui1.py      # Streamlit app variant
├── README.md
├── requirements.txt            # Optional dependency list
├── .env                        # Local API key (create this yourself)
└── .gitignore
```

Run the Streamlit file you want to use. The two UI files are alternative app entry points; you only need to start one at a time.

## Prerequisites

- Python 3.9 or later
- A [Mistral AI API key](https://console.mistral.ai/)

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AI-Resume-Builder
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the repository includes `requirements.txt`:

```bash
pip install -r requirements.txt
```

Otherwise, install the libraries used by the app:

```bash
pip install streamlit langchain langchain-mistralai python-dotenv
```

## Configure Your Mistral API Key

Create a file named `.env` in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

The app loads this value locally to authenticate requests to Mistral AI.

Add the following to `.gitignore` before committing your project:

```gitignore
.env
.venv/
__pycache__/
```

## Run the App

Start either Streamlit UI:

```bash
streamlit run resumegenerator_ui.py
```

or:

```bash
streamlit run resumegenerator_ui1.py
```

Streamlit will open the application in your browser, usually at `http://localhost:8501`.

## How to Use

1. Open the app in your browser.
2. Select one of the available Mistral model options in the sidebar or model selector.
3. Fill in your personal, education, skill, and experience details.
4. Click the resume-generation button.
5. Review the generated plain-text resume.
6. Use the download button to save it as a `.txt` file.

## Workflow

```text
Candidate details entered in Streamlit
              ↓
Prompt assembled with LangChain
              ↓
Selected Mistral model generates resume text
              ↓
ATS-friendly plain-text resume shown in the app
              ↓
Downloaded as a .txt file
```

## Model Options

The app exposes a selector for the Mistral model options configured in the UI source. Choose the model that best suits your desired balance of speed and output quality before generating a resume. Available options may depend on your Mistral account and API access.

## ATS-Friendly Output

The generation prompt is designed to produce a readable, conventional resume structure using plain text. It focuses on clearly organized sections and avoids decorative formatting that can interfere with applicant tracking systems.

Always review the result before applying: confirm dates, facts, contact details, and job-specific wording. AI-generated content should reflect only information you can support.

## Security Note

- Never commit your `.env` file or API key.
- If a key is exposed, revoke it in the Mistral console and create a replacement.
- Resume details may be sent to Mistral AI for generation. Avoid entering sensitive information you do not want processed by that service.

## Future Improvements

- Add selectable resume layouts and style presets
- Tailor resumes to a pasted job description
- Add keyword matching and ATS feedback
- Allow users to save and revisit drafts
- Add input validation and richer experience/project forms
- Offer export to DOCX and PDF
- Add automated tests and deployment guidance

## License
 MIT License.
