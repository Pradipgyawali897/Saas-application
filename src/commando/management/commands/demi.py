import os
import shutil
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Deletes all migration files and __pycache__ folders, then runs makemigrations and migrate.'

    def handle(self, *args, **kwargs):
        base_dir = os.getcwd()
        self.stdout.write("🔍 Scanning project...")

        deleted_migrations = 0
        deleted_pycache = 0

        for root, dirs, files in os.walk(base_dir, topdown=True):
            # Clean __pycache__ folders
            for d in list(dirs):
                if d == '__pycache__':
                    pycache_path = os.path.join(root, d)
                    shutil.rmtree(pycache_path, ignore_errors=True)
                    dirs.remove(d)  # Prevent descending into it
                    deleted_pycache += 1
                    self.stdout.write(f"🧹 Deleted __pycache__: {pycache_path}")

            # Clean migration files (but keep __init__.py)
            if os.path.basename(root) == 'migrations':
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        deleted_migrations += 1
                        self.stdout.write(f"🗑️ Deleted migration: {file_path}")

        self.stdout.write(f"\n✅ Removed {deleted_migrations} migration file(s) and {deleted_pycache} __pycache__ folder(s).")

        self.stdout.write("⚙️ Running makemigrations...")
        call_command('makemigrations')

        self.stdout.write("⚙️ Running migrate...")
        call_command('migrate')

        self.stdout.write("✅ Reset and migration complete.")
