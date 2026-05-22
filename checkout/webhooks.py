import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for and handle webhooks from Stripe."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    wh_secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    handler = StripeWH_Handler(request)

    event_map = {
        'payment_intent.succeeded': (
            handler.handle_payment_intent_succeeded
        ),
        'payment_intent.payment_failed': (
            handler.handle_payment_intent_payment_failed
        ),
    }

    event_handler = event_map.get(
        event['type'], handler.handle_event
    )
    return event_handler(event)
