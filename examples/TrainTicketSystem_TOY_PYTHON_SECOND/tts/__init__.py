# TrainTicketSystem - SECOND Version (Good Architecture)
# Repository pattern, no cycles, low coupling


def __getattr__(name: str):
    """PEP 562 lazy re-export.

    Failure-mode fixture R5 (module __getattr__): when another file does
    ``from tts import BookingService``, Python calls this function at runtime,
    which lazily imports from tts.booking_service.  Static analysis sees only
    an attribute access on the ``tts`` package — the real dependency on
    ``tts.booking_service`` is invisible.
    """
    if name == "BookingService":
        from tts.booking_service import BookingService
        return BookingService
    raise AttributeError(f"module 'tts' has no attribute {name!r}")
