import logging
import traceback

from django.views.generic import TemplateView

from .apps import ProductsConfig

logger = logging.getLogger(ProductsConfig.name)


class ProductTemplateView(TemplateView):
    template_name = 'products/products_template.html'

    def raise_function(self):
        raise ValueError('Get Value Error Raise')

    def get_context_data(self, **kwargs):
        try:
            self.raise_function()
        except ValueError:
            logger.error(f'I get error - "{traceback.format_exc()}"')
        return super().get_context_data(**kwargs)
