def show_queue_items():
    from celery.app.control import Inspect

    # Inspect all nodes.
    i = Inspect()

    # Show the items that have an ETA or are scheduled for later processing
    i.scheduled()

    # Show tasks that are currently active.
    i.active()

    # Show tasks that have been claimed by workers
    i.reserved()