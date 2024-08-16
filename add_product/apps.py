from django.apps import AppConfig


class AddProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'add_product'

    def ready(self):
        from add_product.models.signals.good_update import (
            update_user_status, 
            clear_pairs, 
            clear_matrix,
            update_priority
        )
