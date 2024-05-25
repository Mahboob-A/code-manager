from django.core.management.base import BaseCommand
from core_apps.code_result.mq_callback import main


class Command(BaseCommand):
    '''Consumes Messages from Code Execution Result Queue 
       Published by RCE Engine Service.
    '''
    help = "Consumes messages from RabbitMQ Code EXEC Result Queue"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Consuming messages from Code EXEC Result Queue...")
        )
        main()
