from shiny import App, ui, render, reactive
import os

app_ui = ui.page_fluid(
    ui.h2("File System Security Test"),
    ui.p("This app attempts to write to the protected /mnt/dynamic-mounts directory."),
    ui.hr(),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_action_button("write_file", "Write to Protected Directory"),
            ui.hr(),
            ui.p("Expected result: Permission denied")
        ),
        
        ui.div(
            ui.h3("Test Results:"),
            ui.div(
                ui.strong("Write attempt status:"), 
                ui.output_text_verbatim("write_status"),
                style="margin: 20px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px;"
            ),
            ui.div(
                ui.strong("File existence check:"), 
                ui.output_text_verbatim("file_exists"),
                style="margin: 20px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px;"
            )
        )
    )
)

def server(input, output, session):
    protected_file_path = "/mnt/dynamic-mounts/test-file.txt"
    
    @output
    @render.text
    def write_status():
        if input.write_file():
            try:
                with open(protected_file_path, "w") as f:
                    f.write("This should not be allowed")
                return "SUCCESS - File was written (SECURITY ISSUE!)"
            except Exception as e:
                return f"EXPECTED ERROR - {str(e)}"
        return "No write attempt yet"
    
    @output
    @render.text
    def file_exists():
        if input.write_file():
            if os.path.exists(protected_file_path):
                return f"File exists at {protected_file_path} (SECURITY ISSUE!)"
            else:
                return "File does not exist (Expected result)"
        return "No check performed yet"

app = App(app_ui, server)
