import os
import time
from io import BytesIO

import gradio as gr
import pandas as pd
import requests

EXCEL_URL = os.environ.get("EXCEL_URL")

def load_data():
    if not EXCEL_URL:
        return pd.DataFrame({"error": ["EXCEL_URL secret is not set"]})
    try:
        r = requests.get(f"{EXCEL_URL}&t={int(time.time())}", timeout=30)
        r.raise_for_status()
        return pd.read_excel(BytesIO(r.content))
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

with gr.Blocks(title="Excel Viewer") as demo:
    gr.Markdown("# 📊 Excel Data Viewer")
    gr.Markdown("Data is pulled live from OneDrive. Click Refresh to re-fetch.")
    table = gr.Dataframe(value=load_data(), interactive=False, wrap=True)
    gr.Button("🔄 Refresh").click(load_data, outputs=table)

demo.launch()
