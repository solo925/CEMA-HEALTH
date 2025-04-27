import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
import subprocess

class Command(BaseCommand):
    help = 'Backup PostgreSQL database'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        backup_file = os.path.join(settings.BACKUP_ROOT, f'backup-{timestamp}.sql')
        
        if db_settings['ENGINE'] == 'django.db.backends.sqlite3':
            # SQLite backup
            self.stdout.write('Backing up SQLite database...')
            db_path = db_settings['NAME']
            backup_command = f'sqlite3 {db_path} .dump > {backup_file}'
        
        elif db_settings['ENGINE'] == 'django.db.backends.postgresql':
            # PostgreSQL backup
            self.stdout.write('Backing up PostgreSQL database...')
            env = os.environ.copy()
            env['PGPASSWORD'] = db_settings.get('PASSWORD', '')
            
            backup_command = [
                'pg_dump',
                '-h', db_settings.get('HOST', 'localhost'),
                '-p', str(db_settings.get('PORT', '5432')),
                '-U', db_settings.get('USER', 'postgres'),
                '-d', db_settings.get('NAME', ''),
                '-f', backup_file,
                '--format=c'  # Custom format for more features
            ]
            
            try:
                subprocess.run(backup_command, env=env, check=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully backed up database to {backup_file}'))
                return backup_file
            except subprocess.CalledProcessError as e:
                self.stdout.write(self.style.ERROR(f'Backup failed: {e}'))
                return None
        
        else:
            self.stdout.write(self.style.ERROR(f'Unsupported database engine: {db_settings["ENGINE"]}'))
            return None