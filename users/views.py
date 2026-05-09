import logging

from django.views.generic import TemplateView

from .apps import UsersConfig

logger = logging.getLogger(UsersConfig.name)


class UserTemplateView(TemplateView):
    template_name = 'users/users_template.html'

    def get_context_data(self, **kwargs):
        logger.debug(f'I see kwargs data of user - "{kwargs}"')
        logger.info(f'get_context_data return data soon...')
        return super().get_context_data(**kwargs)
