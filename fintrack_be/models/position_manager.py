from django.db import models, transaction


class PositionManager(models.Manager):
    def create(self, *args, **kwargs):
        with transaction.atomic():
            position = self.model(kwargs)
            position.save()
            cost = self.kwargs['open_price'] * self.kwargs['quantity']
            position.user.update_funds(cost)