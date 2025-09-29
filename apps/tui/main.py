from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button

class MiTUI(App):
    CSS = """
    Screen { align: center middle; }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("TUI - Sociedad Científica\n\nPresiona el botón para iniciar web (si deseas).", id="texto")
        yield Button("Iniciar web (ejecuta run.py)", id="open")
        yield Footer()

    async def on_button_pressed(self, event):
        if event.button.id == "open":
            import subprocess
            # esto intentará ejecutar run.py en segundo plano
            subprocess.Popen(["python", "run.py"])

if __name__ == "__main__":
    MiTUI().run()
