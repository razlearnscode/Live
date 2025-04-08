from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
import json
from wishlist.models import Deck, Wishlist, Card
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    decks = Deck.objects.prefetch_related('cards').all()

    data = []
    for deck in decks:
        data.append({
            "deck_id": deck.name,
            "cards": [
                {
                    "id": card.id,
                    "name": card.name,
                    "type": card.type,
                    "stage": card.stage,
                    "image_url": card.image_url,
                    "local_image_path": card.local_image_path
                }
                for card in deck.cards.all()
            ]
        })

    # Pass as JSON string
    return render(request, "wishlist/index.html", {
        "decks_json": json.dumps(data, cls=DjangoJSONEncoder)
    })

def show_wishlist(request):

    decks = Deck.objects.prefetch_related('cards').all()
    data = [deck.serialize() for deck in decks]
    return JsonResponse(data, safe=False)


def add_to_wishlist(request, card_id):
     pass

def remove_from_wishlist(request, card_id):

    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'DELETE':
        try:
            wishlist_entry = Wishlist.objects.get(card=card)
            wishlist_entry.delete()
            return JsonResponse({"message": "Removed from wishlist successfully"}, status=200)
        except Wishlist.DoesNotExist:
            return JsonResponse({"message": "Card was not in the wishlist"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

        
