from django.core.management.base import BaseCommand
from wishlist.models import Card


class Command(BaseCommand):
    help = 'Clean and normalize type and stage values for existing cards'

    def handle(self, *args, **options):
        updated = 0

        for card in Card.objects.all():
            original_type = card.type
            original_stage = card.stage

            # Normalize the type value
            raw_type = (card.type or "").strip().lower()
            new_type = None
            if "trainer" in raw_type:
                new_type = "TRAINER"
            elif "pokemon" in raw_type or "pokémon" in raw_type or "pok\u00e9mon" in raw_type:
                new_type = "POKÉMON"

            # Normalize the stage value
            raw_stage = (card.stage or "").strip().lower()
            new_stage = None
            if "basic" in raw_stage:
                new_stage = "BASIC"
            elif "stage 1" in raw_stage:
                new_stage = "STAGE1"
            elif "stage 2" in raw_stage:
                new_stage = "STAGE2"
            elif "supporter" in raw_stage:
                new_stage = "OTHERS"

            # Only update if changed
            if card.type != new_type or card.stage != new_stage:
                card.type = new_type
                card.stage = new_stage
                card.save()
                updated += 1
                self.stdout.write(f"✅ Updated: {card.name} (id: {card.id})")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Cleanup complete! {updated} cards updated."))
