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

    if uploaded_file is not None:
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

    if st.button("Generate Document", type="primary"):
        if not query:
            st.warning("Please enter a generation request.")
            return

        with st.spinner("Generating document..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/generate",
                    json={"query": query},
                    timeout=120,
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
                    status = "✓" if present else "✗"
                    color = "green" if present else "red"
                    st.markdown(f"- {status} **{section}**")

                # Full JSON report
                with st.expander("View full validation report (JSON)"):
                    st.json(validation)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to API. Please make sure the API server is running on http://localhost:8000"
                )
            except requests.exceptions.RequestException as e:
                st.error(f"Error generating document: {e}")
                if hasattr(e, "response") and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        st.error(f"Details: {error_detail.get('detail', 'Unknown error')}")
                    except Exception:
                        pass


def validate_page() -> None:
    """Page for document validation."""
    st.header("Document Validation")

    st.write("Paste or type a document to validate its structure and completeness.")

    text_input = st.text_area(
        "Document text",
        placeholder="Paste your document here...",
        height=300,
    )

    if st.button("Validate Document", type="primary"):
        if not text_input:
            st.warning("Please enter a document to validate.")
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
                    status = "✓" if present else "✗"
                    color = "green" if present else "red"
                    st.markdown(f"- {status} **{section}**")

                # Full JSON report
                with st.expander("View full validation report (JSON)"):
                    st.json(validation)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to API. Please make sure the API server is running on http://localhost:8000"
                )
            except requests.exceptions.RequestException as e:
                st.error(f"Error validating document: {e}")


if __name__ == "__main__":
    main()

