# AI-AUTOMATION-TOOLKIT

An open collection of specialized skills and workflows designed for AI agents to automate tasks involving documents, web applications, and data processing. This toolkit is model-agnostic and built to be easily integrated into various agent frameworks.

## 🚀 Vision

The goal of the **AI-AUTOMATION-TOOLKIT** is to provide a robust, open-source library of capabilities that developers can use to empower their AI agents. Instead of being bound to a specific model or platform, these skills are designed to be flexible, reusable, and customizable.

## 📦 Available Skills

The toolkit is organized into specialized "skills," each focusing on a specific domain or file type:

*   **📄 docx**: Comprehensive creation, editing, and analysis of Word documents. Supports tracked changes, comments, and redlining workflows.
*   **📑 pdf**: A toolkit for manipulating PDF documents, including merging, splitting, text extraction, form filling, and OCR.
*   **📊 xlsx**: Advanced spreadsheet handling with support for formula preservation, complex formatting, and financial modeling.
*   **📽️ pptx**: Presentation automation tools for creating slides from HTML, editing existing decks, and managing templates.
*   **🧪 webapp-testing**: Utilities for testing and automating interactions with local and remote web applications using Playwright.
*   **🎨 frontend-design**: Guidelines and workflows for generating high-quality, aesthetically pleasing frontend code.
*   **🛠️ skill-creator**: A meta-skill guide and toolkit for creating, packaging, and maintaining your own custom skills.

## 🛠️ Prerequisites

To fully utilize all skills in this toolkit, you will need the following installed on your system:

*   **Python 3.8+**
*   **Node.js & npm** (for certain JavaScript-based tools)
*   **LibreOffice** (required for reliable format conversion to PDF)
*   **Poppler** (required for PDF image extraction tools like `pdftoppm`)
*   **Tesseract OCR** (optional, for OCR capabilities)

## 📥 Installation & Getting Started

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/AI-AUTOMATION-TOOLKIT.git
    cd AI-AUTOMATION-TOOLKIT
    ```

2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Explore and Customize**:
    Navigate to the `.agents/skills` directory to explore the available skills. Each skill folder contains a `SKILL.md` file with detailed usage instructions and workflows.
    
    You are encouraged to:
    *   Pick and choose the specific skills you need.
    *   Modify the scripts and workflows to fit your specific use case.
    *   Integrate them into your own agent's configuration.

## 🤝 Contribution

Contributions are welcome! If you want to add a new skill or improve an existing one:

1.  Check out the **skill-creator** skill for guidelines on structure and best practices.
2.  Fork the repository and create a separate branch.
3.  Ensure your additions are model-agnostic and flexible.
4.  Submit a pull request.

## 📄 License

**AI-AUTOMATION-TOOLKIT LICENSE**

Copyright (c) 2026 Saniul

This project is open-source for personal and internal business use (Charity Work). 
**Commercial use and monetization require explicit permission.** 
Please see the [LICENSE](LICENSE) file for full terms and conditions.

## ⚠️ Disclaimer

This toolkit is a work-in-progress. While the skills and workflows are designed to be stable, users are advised to review the code and understand the actions being performed before running them in production environments. Usage is at your own risk.
