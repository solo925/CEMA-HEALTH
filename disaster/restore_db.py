import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Restore database from backup'

    def add_arguments(self, parser):
        parser.add_argument('backup_file', type=str, help='Path to the backup file')

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        
        if not os.path.exists(backup_file):
            raise CommandError(f'Backup file {backup_file} does not exist')
        
        db_settings = settings.DATABASES['default']
        
        if db_settings['ENGINE'] == 'django.db.backends.sqlite3':
            # SQLite restoration
            self.stdout.write('Restoring SQLite database...')
            db_path = db_settings['NAME']
            # Make sure the database exists
            if os.path.exists(db_path):
                os.remove(db_path)
            restore_command = f'sqlite3 {db_path} < {backup_file}'
            os.system(restore_command)
            
        elif db_settings['ENGINE'] == 'django.db.backends.postgresql':
            # PostgreSQL restoration
            self.stdout.write('Restoring PostgreSQL database...')
            env = os.environ.copy()
            env['PGPASSWORD'] = db_settings.get('PASSWORD', '')
            
            restore_command = [
                'pg_restore',
                '-h', db_settings.get('HOST', 'localhost'),
                '-p', str(db_settings.get('PORT', '5432')),
                '-U', db_settings.get('USER', 'postgres'),
                '-d', db_settings.get('NAME', ''),
                '-c',  # Clean (drop) database objects before recreating
                backup_file
            ]
            
            try:
                subprocess.run(restore_command, env=env, check=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully restored database from {backup_file}'))
            except subprocess.CalledProcessError as e:
                self.stdout.write(self.style.ERROR(f'Restoration failed: {e}'))
        
        else:
            self.stdout.write(self.style.ERROR(f'Unsupported database engine: {db_settings["ENGINE"]}'))