import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from wishlist.models import Deck, Card, Wishlist


class Command(BaseCommand):
    help = 'Import wishlist cards from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='Path to the CSV file (e.g. wishlist.csv)'
        )

    def handle(self, *args, **options):
        file_path = Path(options['file'])

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return

        added = 0
        skipped = 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                deck_id = row.get("deck_id")
                card_id = row.get("card_id")

                if not deck_id or not card_id:
                    self.stdout.write(self.style.WARNING("⚠️ Skipping row with missing deck_id/card_id"))
                    continue

                try:
                    card = Card.objects.get(deck__deck_id=deck_id, card_id=card_id)
                except Card.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"⚠️ Card not found: Deck {deck_id}, Card {card_id}"))
                    continue

                wishlist_item, created = Wishlist.objects.get_or_create(card=card)
                if created:
                    added += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Added to wishlist: {card.name}"))
                else:
                    skipped += 1
                    self.stdout.write(f"⏭️ Already in wishlist: {card.name}")

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Wishlist import complete! Added: {added}, Skipped: {skipped}"
        ))
