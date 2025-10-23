import schedule
import time
from datetime import datetime, timedelta
from threading import Thread

class BackupService:
    """Serviço de backup automático"""
    
    def __init__(self, db):
        self.db = db
    
    def create_backup(self):
        """Cria backup dos dados"""
        try:
            backup_date = datetime.utcnow()
            backup_name = f"backup_{backup_date.strftime('%Y%m%d_%H%M%S')}"
            
            collections = ["usuarios", "entradas", "saidas", "apis"]
            backup_data = {}
            
            for collection_name in collections:
                collection = getattr(self.db, collection_name)
                documents = list(collection.find({}))
                
                # Converter ObjectId para string
                for doc in documents:
                    doc["_id"] = str(doc["_id"])
                
                backup_data[collection_name] = documents
            
            backup_document = {
                "backup_name": backup_name,
                "data": backup_data,
                "created_at": backup_date,
                "collections_count": {name: len(data) for name, data in backup_data.items()}
            }
            
            self.db.backups.insert_one(backup_document)
            print(f"✅ Backup criado: {backup_name}")
            
            # Limpar backups antigos (manter apenas últimos 30 dias)
            cutoff_date = backup_date - timedelta(days=30)
            self.db.backups.delete_many({"created_at": {"$lt": cutoff_date}})
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {str(e)}")
    
    def schedule_backups(self):
        """Agenda backups automáticos"""
        schedule.every().day.at("02:00").do(self.create_backup)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        # Executar scheduler em thread separada
        scheduler_thread = Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()