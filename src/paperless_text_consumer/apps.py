# -*- coding: utf-8 -*-

from django.apps import AppConfig


class PaperlessTextConsumerConfig(AppConfig):

    name = "paperless_text_consumer"

    def ready(self):
        from documents.signals import document_consumer_declaration
        from .signals import ConsumerDeclaration
        print('connecting signal')
        document_consumer_declaration.connect(ConsumerDeclaration.handle)
        AppConfig.ready(self)
        print('app is ready')
