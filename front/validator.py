from typing import Dict


def validate_form(form_data: Dict) -> bool:
    mode = form_data.get("mode")

    if mode == "hard":
        competitors = form_data.get("competitors")

        if not competitors:
            required_fields = {
                "queries": list,
                "exclude_domains": list,
                "search_engine": str,
                "device": str,
                "lr": int,
                "loc": int,
                "user_agent": str,
                "exclude_tags": list,
            }
        else:
            required_fields = {
                "queries": list,
                "competitors": list,
                "user_agent": str,
                "exclude_tags": list,
            }

        for field, expected_type in required_fields.items():
            if field not in form_data:
                return False

            value = form_data[field]

            if value is None:
                continue

            if not isinstance(value, expected_type):
                return False

            if isinstance(value, list) and field == "queries" and len(value) == 0:
                return False

        return True


    elif mode == "easy":
        prompt = form_data.get("additional_prompt")
        return bool(prompt and prompt.strip())

    else:
        return False
