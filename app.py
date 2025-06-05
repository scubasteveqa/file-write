from shiny import App, ui, render, reactive
import os
import traceback
import sys
from io import StringIO

# Use page_sidebar instead of layout_sidebar to make the sidebar visible by default
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_action_button("write_file", "Write to Protected Directory", 
                               width="100%",  # Make button full width
                               class_="btn-lg"),  # Make button larger
        ui.hr(),
        ui.p("Expected result: Permission denied"),
        open="always"  # This ensures the sidebar is open by default
    ),
    
    ui.h2("File System Security Test"),
    ui.p("This app attempts to write to the protected /mnt/dynamic-mounts directory."),
    ui.hr(),
    
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
    ),
    ui.div(
        ui.strong("Detailed Error Logs:"), 
        ui.output_text_verbatim("error_logs"),
        style="margin: 20px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px; background-color: #f8f8f8; font-family: monospace; white-space: pre-wrap;"
    )
)

def server(input, output, session):
    protected_file_path = "/mnt/dynamic-mounts/test-file.txt"
    
    # Reactive value to store detailed error logs
    error_log = reactive.value("")
    
    @output
    @render.text
    def write_status():
        if input.write_file():
            try:
                with open(protected_file_path, "w") as f:
                    f.write("This should not be allowed")
                return "SUCCESS - File was written (SECURITY ISSUE!)"
            except Exception as e:
                # Capture detailed exception information
                error_buffer = StringIO()
                traceback.print_exc(file=error_buffer)
                error_log.set(f"Exception type: {type(e).__name__}\nError message: {str(e)}\n\nTraceback:\n{error_buffer.getvalue()}")
                
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
    
    @output
    @render.text
    def error_logs():
        if input.write_file() and error_log.get():
            return error_log.get()
        elif input.write_file():
            return "No errors captured (file was successfully written - SECURITY ISSUE!)"
        return "No write attempt yet"

app = App(app_ui, server)
