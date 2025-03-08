import os
import hashlib
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from api.models.models import Manifest


class Command(BaseCommand):
    help = 'Generates manifest entries with MD5 hashes for data files'

    def handle(self, *args, **kwargs):
        data_dirs = [
            os.path.join(os.getcwd(), 'data', 'v1'),
            os.path.join(os.getcwd(), 'data', 'v2'),
        ]
        
        # Clear existing manifests
        Manifest.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing manifests'))
        
        file_count = 0
        
        for data_dir in data_dirs:
            if not os.path.exists(data_dir):
                self.stdout.write(self.style.WARNING(f'Directory {data_dir} does not exist'))
                continue
                
            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, os.getcwd())
                        
                        try:
                            # Calculate MD5 hash of the file contents
                            with open(file_path, 'rb') as f:
                                file_hash = hashlib.md5(f.read()).hexdigest()
                            
                            # Determine the type based on the filename or directory
                            file_type = Path(file).stem
                            
                            # Create manifest entry
                            Manifest.objects.create(
                                filename=rel_path,
                                type=file_type,
                                hash=file_hash
                            )
                            
                            file_count += 1
                            
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error processing {file_path}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Generated manifest entries for {file_count} files'))