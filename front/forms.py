from typing import Dict, Optional

import streamlit as st


def serp_parsing_form() -> Optional[Dict]:
    with st.form("serp_parsing_form"):
        mode = st.selectbox("Выберите режим", ("easy", "hard"))

        model = st.selectbox("Укажите модель генерации ТЗ",
                             ("openai/gpt-oss-20b:free", "deepseek/deepseek-chat-v3.1:free", "x-ai/grok-4-fast:free"))
        additional_prompt = st.text_area("Введите дополнительные данные для генерации")
        temperature = st.slider("Температура генерации", 0.0, 2.0, 0.5, 0.05)

        with st.expander("Экспертные настройки для hard режима"):
            queries = st.text_area("Укажите поисковые запросы")
            competitors = st.text_area("Укажите конкурентов (опционально)")
            search_engine = st.selectbox("Выберите поисковую систему", ("Yandex", "Google"))
            device = st.selectbox("Выберите устройство", ("desktop", "mobile"))
            lr = st.number_input("Выберите регион для Яндекс", step=1, value=213)
            loc = st.number_input("Выберите регион для Google", step=1, value=20950)
            exclude_domains = st.text_area("Укажите домены для исключения (опционально)")
            exclude_tags = st.text_area(
                "Укажите теги, которые нужно исключить из анализа",
                value="\n".join(['script', 'style', 'nav', 'footer', 'header', 'aside', 'meta', 'link'])
            )
            user_agent = st.text_input(
                "Укажите User-Agent",
                value=("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/W.X.Y.Z Mobile Safari/537.36 "
                       "(compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
            )
            doc_type = st.selectbox("Укажите тип документа", ("Article", "Service", "Listing", "Card"))

        submitted = st.form_submit_button("Сгенерировать ТЗ")

        if submitted:
            return {
                "mode": mode,
                "queries": [q.strip() for q in queries.split("\n") if q.strip()],
                "competitors": [c.strip() for c in competitors.split("\n") if c.strip()],
                "search_engine": search_engine,
                "device": device,
                "lr": lr,
                "loc": loc,
                "exclude_domains": [d.strip() for d in exclude_domains.split("\n") if d.strip()],
                "exclude_tags": [t.strip() for t in exclude_tags.split("\n") if t.strip()],
                "user_agent": user_agent,
                "model": model,
                "doc_type": doc_type,
                "additional_prompt": additional_prompt.strip() if additional_prompt else None,
                "temperature": temperature
            }
    return None
