import streamlit as st

from core import TaskGenerator, TextGenerator
from front import faq, serp_parsing_form, validate_form
from utils import create_word_file, name_report_file

st.title("📊 Article FLow")
with st.expander("📘 Инструкция по использованию"):
    st.markdown(faq)

if "technical_task" not in st.session_state:
    st.session_state.technical_task = None

form_data = serp_parsing_form()

if form_data and validate_form(form_data):
    with st.spinner("Формируется ТЗ, подождите..."):
        task_generator = TaskGenerator(**form_data)
        top_urls, st.session_state.technical_task = task_generator.generate()
        st.session_state.model = form_data["model"]
        st.session_state.temperature = form_data["temperature"]

    if st.session_state.technical_task:

        if top_urls:
            st.subheader("URL для анализа")
            for url in top_urls:
                st.write(f"- {url}")

        file_name = name_report_file(form_data)
        st.session_state.file_name = file_name
        file_stream = create_word_file(
            title="Техническое задание",
            paragraphs=[st.session_state.technical_task]
        )
        st.download_button(
            label="📥 Скачать ТЗ в формате Word",
            data=file_stream,
            file_name=f"{file_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

if st.session_state.technical_task:
    with st.form("write_text_form"):
        st.markdown("### Сгенерировать текст по готовому ТЗ")
        submitted_text = st.form_submit_button("🚀 Сгенерировать текст")

        if submitted_text:
            with st.spinner("Генерируется текст..."):
                text_generator = TextGenerator(
                    model=st.session_state.model,
                    temperature=st.session_state.temperature
                )
                final_text = text_generator.generate(st.session_state.technical_task)
                st.session_state.final_text = final_text

if "final_text" in st.session_state:
    st.markdown("### 📝 Сгенерированный текст:")
    st.write(st.session_state.final_text)

    text_file_stream = create_word_file(
        title="Сгенерированный текст",
        paragraphs=[st.session_state.final_text]
    )
    st.download_button(
        label="📥 Скачать текст в Word",
        data=text_file_stream,
        file_name=f"{st.session_state.file_name}_text.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
