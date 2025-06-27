import graphene

from ....attribute import models as models
from ....permission.enums import ProductTypePermissions
from ....webhook.event_types import WebhookEventAsyncType
from ...core import ResolveInfo
from ...core.mutations import ModelDeleteMutation, ModelWithExtRefMutation
from ...core.types import AttributeError
from ...core.utils import WebhookEventInfo
from ...plugins.dataloaders import get_plugin_manager_promise
from ..types import Attribute


class AttributeDelete(ModelDeleteMutation, ModelWithExtRefMutation):
    class Arguments:
        id = graphene.ID(required=False, description="ID of an attribute to delete.")
        external_reference = graphene.String(
            required=False,
            description="External ID of an attribute to delete.",
        )

    class Meta:
        model = models.Attribute
        object_type = Attribute
        description = "Deletes an attribute."
        permissions = (ProductTypePermissions.MANAGE_PRODUCT_TYPES_AND_ATTRIBUTES,)
        error_type_class = AttributeError
        error_type_field = "attribute_errors"
        webhook_events_info = [
            WebhookEventInfo(
                type=WebhookEventAsyncType.ATTRIBUTE_DELETED,
                description="An attribute was deleted.",
            ),
        ]

    @classmethod
    def post_save_action(cls, info: ResolveInfo, instance, cleaned_input):
        manager = get_plugin_manager_promise(info.context).get()
        cls.call_event(manager.attribute_deleted, instance)

    @classmethod
    def perform_mutation(cls, _root, info: ResolveInfo, /, **data):
        instance = cls.get_instance(info, **data)
        user = info.context.user
        if user and user.is_authenticated:
            store = instance.metadata.get("store")
            if store != user.first_name:
                from django.core.exceptions import ValidationError
                raise ValidationError("You do not have permission to delete this object.")
        return super().perform_mutation(_root, info, **data)
