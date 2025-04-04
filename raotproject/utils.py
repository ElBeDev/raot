import json
import uuid
from django.core.serializers.json import DjangoJSONEncoder

class UUIDEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode UUID objects.
    """
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # Return a string representation of the UUID
            return str(obj)
        return super().default(obj)

# Use this function anywhere you need to serialize objects containing UUIDs
def json_dumps(obj):
    return json.dumps(obj, cls=UUIDEncoder)