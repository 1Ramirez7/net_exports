from shiny import App, ui, render, reactive
import pandas as pd

# Load CSV from URL
DATA_URL = "https://raw.githubusercontent.com/1Ramirez7/net_exports/main/raw_data/2015-2024_trade_balance_all_commodities.csv"
df = pd.read_csv(DATA_URL)

# Get column names
column_names = df.columns.tolist()

# 1) Define the UI
app_ui = ui.page_fluid(
    ui.h2("CSV Variable Selector with Unique Values"),
    ui.input_checkbox_group("columns", "Select columns:", choices=column_names),
    ui.output_ui("unique_values")
)

# 2) Define server logic
def server(input, output, session):
    @output
    @render.ui
    def unique_values():
        selected = input.columns()
        if not selected:
            return ui.p("No columns selected.")

        # Create a section for each selected column with its unique values
        output_blocks = []
        for col in selected:
            unique_vals = df[col].dropna().unique().tolist()
            # Convert to string to avoid rendering issues with numbers or NaNs
            formatted = [str(val) for val in unique_vals[:20]]  # limit to 20 for brevity
            output_blocks.append(
                ui.div(
                    ui.h4(f"Unique values for: {col}"),
                    ui.tags.ul(*[ui.tags.li(v) for v in formatted])
                )
            )
        return ui.div(*output_blocks)

# 3) Create app object
app = App(app_ui, server)
