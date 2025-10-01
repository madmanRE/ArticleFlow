import re
from typing import Dict


def name_report_file(form_data: Dict) -> str:
    if form_data.get("queries"):
        file_name = form_data["queries"][0]
    elif form_data.get("additional_prompt"):
        file_name = form_data["additional_prompt"][:min(20, len(form_data["additional_prompt"]))]
    else:
        file_name = "technical_task"

    file_name = re.sub(r'[\\/*?:"<>|]', "", file_name).strip()
    return file_name