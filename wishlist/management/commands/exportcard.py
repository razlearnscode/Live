import csv
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from wishlist.models import Card


class Command(BaseCommand):
    help = 'Export all cards to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Path to output CSV file (relative to media/)',
            default='cards_export.csv'
        )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        output_path = media_root / options['output']

        # Create parent folders if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cards = Card.objects.select_related('deck').all()

        with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['deck_id', 'card_id'])  # CSV header

            for card in cards:
                writer.writerow([card.deck.deck_id, card.card_id])

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {cards.count()} cards to: {output_path.resolve()}"))
