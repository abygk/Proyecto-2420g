import json
import os
import re
import typer
from rich.console import Console
from rich.table import Table
import pandas as pd

app = typer.Typer()
console = Console()

DATA_FILE = "data/users.json"
ADMINS_FILE = "data/admins.json"

# Sesión persistente
SESSION = {"admin": None}

# -------------------------------
# Utilidades de validación
# -------------------------------
def validate_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def validate_age(age: int):
    return age >= 10

# -------------------------------
# Manejo de usuarios
# -------------------------------
def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

# -------------------------------
# Manejo de admins
# -------------------------------
def load_admins():
    if not os.path.exists(ADMINS_FILE):
        default_admin = {"usuario": "admin", "password": "1234"}
        os.makedirs("data", exist_ok=True)
        with open(ADMINS_FILE, "w", encoding="utf-8") as f:
            json.dump([default_admin], f, indent=4, ensure_ascii=False)
        return [default_admin]
    with open(ADMINS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def verify_admin():
    admins = load_admins()
    usuario = typer.prompt("Usuario admin")
    password = typer.prompt("Contraseña", hide_input=True)

    for admin in admins:
        if admin["usuario"] == usuario and admin["password"] == password:
            console.print(f"[green]✅ Acceso concedido como {usuario}[/green]")
            SESSION["admin"] = usuario
            return True

    console.print("[red]❌ Credenciales inválidas[/red]")
    raise typer.Exit()

# -------------------------------
# Callback para comandos admin
# -------------------------------
@app.callback()
def main(ctx: typer.Context):
    admin_commands = ["delete_user", "export_excel", "stats"]
    if ctx.invoked_subcommand in admin_commands and not SESSION["admin"]:
        verify_admin()

# -------------------------------
# Comandos de la app
# -------------------------------
@app.command()
def add_user():
    """Agregar un nuevo participante"""
    nombre = typer.prompt("Nombre completo")
    edad = typer.prompt("Edad", type=int)
    if not validate_age(edad):
        console.print("[red]❌ La edad mínima es 10 años[/red]")
        raise typer.Exit()

    correo = typer.prompt("Correo electrónico")
    if not validate_email(correo):
        console.print("[red]❌ Correo inválido[/red]")
        raise typer.Exit()

    categoria = typer.prompt(
        "Categoría",
        type=typer.Choice(["Colegio", "Universidad", "Libre"], case_sensitive=False)
    )
    institucion = typer.prompt("Institución (colegio o universidad)")

    users = load_users()
    if any(u["correo"] == correo for u in users):
        console.print(f"[red]❌ El correo {correo} ya está registrado[/red]")
        raise typer.Exit()

    user = {
        "nombre": nombre,
        "edad": edad,
        "correo": correo,
        "categoria": categoria,
        "institucion": institucion,
    }
    users.append(user)
    save_users(users)
    console.print(f"[green]✅ Usuario {nombre} agregado con éxito[/green]")

@app.command()
def list_users():
    """Mostrar todos los participantes"""
    users = load_users()
    if not users:
        console.print("[yellow]No hay participantes registrados[/yellow]")
        raise typer.Exit()

    table = Table(title="Lista de Participantes")
    table.add_column("Nombre", style="cyan", no_wrap=True)
    table.add_column("Edad", style="magenta")
    table.add_column("Correo", style="green")
    table.add_column("Categoría", style="blue")
    table.add_column("Institución", style="yellow")

    for u in users:
        table.add_row(
            u["nombre"], str(u["edad"]), u["correo"], u["categoria"], u["institucion"]
        )
    console.print(table)

@app.command()
def delete_user(correo: str):
    """Eliminar un participante por correo (solo admin)"""
    users = load_users()
    user = next((u for u in users if u["correo"] == correo), None)
    if not user:
        console.print(f"[red]❌ No se encontró el usuario con correo {correo}[/red]")
        raise typer.Exit()

    confirm = typer.confirm(f"¿Seguro que quieres eliminar a {user['nombre']}?")
    if not confirm:
        console.print("[yellow]Operación cancelada[/yellow]")
        raise typer.Exit()

    users = [u for u in users if u["correo"] != correo]
    save_users(users)
    console.print(f"[green]✅ Usuario con correo {correo} eliminado[/green]")

@app.command()
def export_excel():
    """Exportar participantes a un archivo Excel (solo admin)"""
    users = load_users()
    if not users:
        console.print("[yellow]No hay datos para exportar[/yellow]")
        raise typer.Exit()

    df = pd.DataFrame(users)
    os.makedirs("data", exist_ok=True)
    output_file = "data/participantes.xlsx"
    df.to_excel(output_file, index=False)
    console.print(f"[green]✅ Datos exportados a {output_file}[/green]")

@app.command()
def stats():
    """Mostrar estadísticas de inscripción (solo admin)"""
    users = load_users()
    if not users:
        console.print("[yellow]No hay participantes registrados[/yellow]")
        raise typer.Exit()

    categorias = {}
    for u in users:
        cat = u["categoria"]
        categorias[cat] = categorias.get(cat, 0) + 1

    table = Table(title="Estadísticas por Categoría")
    table.add_column("Categoría", style="cyan")
    table.add_column("Cantidad", style="magenta")

    for cat, count in categorias.items():
        table.add_row(cat, str(count))

    console.print(table)

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    app()
