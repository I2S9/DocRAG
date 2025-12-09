"""Streamlit UI for DocRAG system."""

import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"


def main() -> None:
    """Main Streamlit application."""
    st.title("DocRAG - Technical Document Generator")

    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Generate Document", "Validate Document"])

    if page == "Generate Document":
        generate_page()
    elif page == "Validate Document":
        validate_page()


def generate_page() -> None:
    """Page for document generation."""
    st.header("Document Generation")

    # Document upload section
    st.subheader("1. Upload Document (PDF)")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    # Check API connection
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        api_available = True
    except requests.exceptions.RequestException:
        api_available = False
        st.error(
            "**API Server is not running.**\n\n"
            "Please start the API server first:\n"
            "```bash\n"
            "uvicorn src.api.app:app --reload\n"
            "```\n"
            "Or use:\n"
            "```bash\n"
            "python start_api.py\n"
            "```\n"
            "The API should be running on http://localhost:8000"
        )

    if uploaded_file is not None and api_available:
        if st.button("Index Document"):
            with st.spinner("Indexing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(
                        f"{API_BASE_URL}/index",
                        files=files,
                        timeout=120,
                    )
                    response.raise_for_status()
                    data = response.json()
                    st.success(f"Document indexed successfully! ({data['chunks_count']} chunks)")
                except requests.exceptions.ConnectionError:
                    st.error(
                        "**Cannot connect to API server.**\n\n"
                        "Please make sure the API is running on http://localhost:8000\n\n"
                        "Start it with:\n"
                        "```bash\n"
                        "uvicorn src.api.app:app --reload\n"
                        "```"
                    )
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The document might be too large. Please try again.")
                except requests.exceptions.HTTPError as e:
                    error_detail = "Unknown error"
                    try:
                        error_data = e.response.json()
                        error_detail = error_data.get("detail", str(e))
                    except Exception:
                        error_detail = str(e)
                    st.error(f"Error indexing document: {error_detail}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error indexing document: {e}")

    st.divider()

    # Query input section
    st.subheader("2. Generation Request")
    query = st.text_area(
        "Enter your generation request",
        placeholder="e.g., Generate a technical specification for component X",
        height=100,
    )

    # Check API connection for generation
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        api_available_gen = True
    except requests.exceptions.RequestException:
        api_available_gen = False
        st.warning(
            "**API Server is not running.** Please start the API server first."
        )

    if st.button("Generate Document", type="primary", disabled=not api_available_gen):
        if not query:
            st.warning("Please enter a generation request.")
            return

        if not api_available_gen:
            st.error("Cannot generate document: API server is not available.")
            return

        with st.spinner("Generating document... This may take several minutes..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate",
                    json={"query": query},
                    timeout=300,
                )
                response.raise_for_status()
                data = response.json()

                # Display generated document
                st.divider()
                st.subheader("Generated Document")
                st.text_area(
                    "Document content",
                    value=data["document"],
                    height=400,
                    disabled=True,
                )

                # Display validation report
                st.divider()
                st.subheader("Validation Report")
                validation = data["validation"]

                # Summary
                if validation.get("all_sections_present", False):
                    st.success("All required sections are present")
                else:
                    st.warning("Some required sections are missing")

                # Detailed section status
                st.write("**Section Status:**")
                sections = validation.get("sections", {})
                for section, present in sections.items():
                    status = "[OK]" if present else "[MISSING]"
                    st.markdown(f"- {status} **{section}**")

                # Full JSON report
                with st.expander("View full validation report (JSON)"):
                    st.json(validation)

            except requests.exceptions.ConnectionError:
                st.error(
                    "**Cannot connect to API server.**\n\n"
                    "Please make sure the API is running on http://localhost:8000\n\n"
                    "Start it with:\n"
                    "```bash\n"
                    "uvicorn src.api.app:app --reload\n"
                    "```"
                )
            except requests.exceptions.Timeout:
                st.error(
                    "**Request timed out.**\n\n"
                    "Generation can take several minutes. Possible causes:\n"
                    "- Ollama model is still loading\n"
                    "- The model is too slow for your hardware\n"
                    "- The prompt is too long\n\n"
                    "**Solutions:**\n"
                    "- Wait a bit longer and try again\n"
                    "- Use a smaller/faster model (e.g., llama3:8b instead of llama3)\n"
                    "- Try a shorter query\n"
                    "- Check if Ollama is running: `ollama list`"
                )
            except requests.exceptions.HTTPError as e:
                error_detail = "Unknown error"
                status_code = None
                try:
                    error_data = e.response.json()
                    error_detail = error_data.get("detail", str(e))
                    status_code = e.response.status_code
                except Exception:
                    error_detail = str(e)
                
                if status_code == 504:
                    st.error(
                        f"**Generation Timeout**\n\n"
                        f"{error_detail}\n\n"
                        "**Possible solutions:**\n"
                        "- Use a smaller/faster model (e.g., `llama3:8b`)\n"
                        "- Try a shorter query\n"
                        "- Check if Ollama is running: `ollama list`\n"
                        "- Wait a bit and try again"
                    )
                elif status_code == 503:
                    st.error(
                        f"**Ollama Not Found**\n\n"
                        f"{error_detail}\n\n"
                        "**Installation:**\n"
                        "1. Download from https://ollama.ai/\n"
                        "2. Install and add to PATH\n"
                        "3. Pull a model: `ollama pull llama3`\n"
                        "4. Restart the API"
                    )
                else:
                    st.error(f"Error generating document: {error_detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error generating document: {e}")


def validate_page() -> None:
    """Page for document validation."""
    st.header("Document Validation")

    st.write("Paste or type a document to validate its structure and completeness.")

    text_input = st.text_area(
        "Document text",
        placeholder="Paste your document here...",
        height=300,
    )

    # Check API connection for validation
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        api_available_val = True
    except requests.exceptions.RequestException:
        api_available_val = False
        st.warning(
            "**API Server is not running.** Please start the API server first."
        )

    if st.button("Validate Document", type="primary", disabled=not api_available_val):
        if not text_input:
            st.warning("Please enter a document to validate.")
            return

        if not api_available_val:
            st.error("Cannot validate document: API server is not available.")
            return

        with st.spinner("Validating document..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/validate",
                    json={"text": text_input},
                    timeout=30,
                )
                response.raise_for_status()
                data = response.json()
                validation = data["validation"]

                # Summary
                st.divider()
                st.subheader("Validation Results")

                if validation.get("all_sections_present", False):
                    st.success("All required sections are present")
                else:
                    st.warning("Some required sections are missing")

                # Detailed section status
                st.write("**Section Status:**")
                sections = validation.get("sections", {})
                for section, present in sections.items():
                    status = "[OK]" if present else "[MISSING]"
                    st.markdown(f"- {status} **{section}**")

                # Full JSON report
                with st.expander("View full validation report (JSON)"):
                    st.json(validation)

            except requests.exceptions.ConnectionError:
                st.error(
                    "**Cannot connect to API server.**\n\n"
                    "Please make sure the API is running on http://localhost:8000\n\n"
                    "Start it with:\n"
                    "```bash\n"
                    "uvicorn src.api.app:app --reload\n"
                    "```"
                )
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except requests.exceptions.HTTPError as e:
                error_detail = "Unknown error"
                try:
                    error_data = e.response.json()
                    error_detail = error_data.get("detail", str(e))
                except Exception:
                    error_detail = str(e)
                st.error(f"Error validating document: {error_detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error validating document: {e}")


if __name__ == "__main__":
    main()

