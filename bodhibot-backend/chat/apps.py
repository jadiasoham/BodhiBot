from django.apps import AppConfig

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    # def ready(self):
    #     # Import all the models once to initialize...
    #     from .services.model_manager import (
    #         # inference_model,
    #         # policy_llm,
    #         detox_original,
    #         detox_unbiased,
    #     )

    #     # Import all the gatekeeper layers:
    #     # from .services.gatekeeper_service.layers.keyword_filter_layer import KeywordBasedFilteringLayer
    #     from .services.gatekeeper_service.layers.toxicity_detection_layer import ToxicityDetectionLayer
    #     # from .services.gatekeeper_service.layers.policy_enforcement_layer import PolicyEnforcementLayer
        
    #     return super().ready()
    