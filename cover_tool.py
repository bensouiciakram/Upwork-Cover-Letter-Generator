import sys
import os
from datetime import datetime
import subprocess

TEMPLATES = {
    "web scraping": {
        "label": "Web Scraping",
        "placeholders": [
            ("website_or_niche", "Website / niche (e.g., e-commerce, real estate)"),
            ("client_name", "Client Name"),
            ("target_websites", "Target website(s) (comma-separated or description)"),
            ("output_format", "Preferred output format (CSV / JSON / Excel / Database)"),
            ("tool_stack", "Tool(s) to use (Scrapy / Playwright / BeautifulSoup / Requests or leave blank)"),
            ("urls_to_scrape", "URLs to scrape (paste or describe)"),
            ("fields_to_extract", "Fields to extract (list)"),
            ("your_name", "Your Name"),
        ],
        "render": lambda v: (
            f"Subject: Web Scraping for {v['website_or_niche']}\n"
            f"Hi {v['client_name']},\n"
            f"I can help you scrape data from {v['target_websites']} and output it in {v['output_format']}.\n"
            f"I usually use Python + {v['tool_stack'] or 'Scrapy / Playwright / BeautifulSoup / Requests'} depending on the complexity.\n"
            f"I will handle pagination, dynamic content, error handling, and cleanup.\n"
            f"Details I need from you:\n"
            f"URLs to scrape: {v['urls_to_scrape']}\n"
            f"fields to extract: {v['fields_to_extract']}\n"
            f"output format: {v['output_format']}\n"
            f"Once I get the above, I can give you an exact timeline.\n"
            f"Thanks,\n"
            f"{v['your_name']}\n"
        ),
    },
    "django": {
        "label": "Django",
        "placeholders": [
            ("project_name", "Project name"),
            ("client_name", "Client Name"),
            ("task_feature", "The task / feature (short)"),
            ("extra_tech", "Any extra relevant tech (optional)"),
            ("feature_needed", "What exact feature is needed"),
            ("codebase_access", "Current codebase access (Github / Zip / etc)"),
            ("deployment_env", "Deployment environment (Render / VPS / Other)"),
            ("your_name", "Your Name"),
        ],
        "render": lambda v: (
            f"Subject: Django Backend Help (for {v['project_name']})\n"
            f"Hello {v['client_name']},\n"
            f"I’m a Django developer and I can help you with {v['task_feature']}.\n"
            f"Tech I can work with:\n"
            f"Django\n"
            f"Django REST Framework\n"
            f"PostgreSQL / MySQL / SQLite\n"
            f"{v['extra_tech']}\n"
            f"Please share:\n"
            f"What exact feature is needed: {v['feature_needed']}\n"
            f"Current codebase access: {v['codebase_access']}\n"
            f"Deployment environment: {v['deployment_env']}\n"
            f"I can start once I understand the scope clearly.\n"
            f"Regards,\n"
            f"{v['your_name']}\n"
        ),
    },
    "react": {
        "label": "React",
        "placeholders": [
            ("short_description", "Short subject description"),
            ("client_name", "Client Name"),
            ("feature_bug", "Exact UI/feature/bug you can help with"),
            ("react_or_next", "Is it plain React or Next.js (React / Next.js)"),
            ("repo_access", "Repo / code access (Github link or instructions)"),
            ("your_name", "Your Name"),
        ],
        "render": lambda v: (
            f"Subject: React Feature / Fix – {v['short_description']}\n"
            f"Hi {v['client_name']},\n"
            f"I work with React and I can help you with {v['feature_bug']}.\n"
            f"To make sure I deliver exactly what you expect, I need:\n"
            f"What exactly is the problem / feature: {v['feature_bug']}\n"
            f"Is it plain React or Next.js: {v['react_or_next']}\n"
            f"Repo / code access: {v['repo_access']}\n"
            f"Once I inspect it, I will tell you the best solution and timeline.\n"
            f"Thanks,\n"
            f"{v['your_name']}\n"
        ),
    },
    "python playwright": {
        "label": "Python + Playwright",
        "placeholders": [
            ("site_or_scenario", "Site / scenario"),
            ("client_name", "Client Name"),
            ("exact_task", "Exact task to automate"),
            ("website_name", "Website name / target"),
            ("target_urls", "Target URLs (paste)"),
            ("steps_flow", "Steps to reproduce the flow"),
            ("fields_to_capture", "Fields to capture (if scraping)"),
            ("your_name", "Your Name"),
        ],
        "render": lambda v: (
            f"Subject: Python Playwright Automation for {v['site_or_scenario']}\n"
            f"Hi {v['client_name']},\n"
            f"I specialize in Python + Playwright, and I can automate {v['exact_task']} on {v['website_name']}.\n"
            f"This can include:\n"
            f"logins\n"
            f"form submissions\n"
            f"pagination\n"
            f"data extraction\n"
            f"saving structured output (CSV / JSON / DB)\n"
            f"Please share:\n"
            f"target URLs: {v['target_urls']}\n"
            f"steps to reproduce the flow: {v['steps_flow']}\n"
            f"fields to capture (if scraping): {v['fields_to_capture']}\n"
            f"After I review the site flow, I’ll confirm time + cost.\n"
            f"Best regards,\n"
            f"{v['your_name']}\n"
        ),
    },
}


def prompt_choice():
    print("Select a saved search:")
    options = list(TEMPLATES.keys())
    for idx, key in enumerate(options, start=1):
        print(f"{idx}) {TEMPLATES[key]['label']} ({key})")
    while True:
        choice = input("Enter number (1-4) or name: ").strip().lower()
        if choice.isdigit():
            i = int(choice)
            if 1 <= i <= len(options):
                return options[i - 1]
        if choice in TEMPLATES:
            return choice
        print("Invalid choice. Try again.")


def prompt_placeholders(placeholders):
    values = {}
    for key, prompt in placeholders:
        val = input(f"{prompt}: ").strip()
        values[key] = val
    return values


def timestamped_filename(prefix: str, folder: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prefix = prefix.replace(" ", "_").lower()
    name = f"cover_{safe_prefix}_{ts}.txt"
    return os.path.join(folder, name)


def copy_to_clipboard_windows(text: str):
    try:
        # Use Windows built-in 'clip' command
        proc = subprocess.Popen(
            ["cmd", "/c", "clip"],
            stdin=subprocess.PIPE,
            close_fds=True,
        )
        proc.communicate(input=text.encode("utf-16le"))
    except Exception:
        # Fallback using utf-8 if utf-16le fails
        try:
            proc = subprocess.Popen(["cmd", "/c", "clip"], stdin=subprocess.PIPE, close_fds=True)
            proc.communicate(input=text.encode("utf-8"))
        except Exception:
            print("Warning: Failed to copy to clipboard.")


def main():
    base_folder = os.getcwd()
    choice_key = prompt_choice()
    template = TEMPLATES[choice_key]

    print(f"\nYou selected: {template['label']}\n")
    values = prompt_placeholders(template["placeholders"]) \
        if sys.stdin else {}

    content = template["render"](values)

    out_path = timestamped_filename(template['label'], base_folder)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    copy_to_clipboard_windows(content)

    print("\nGenerated cover letter saved to:")
    print(out_path)
    print("\nThe content has also been copied to your clipboard.")


if __name__ == "__main__":
    main()
