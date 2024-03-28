from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_required(data, fields=None):
        """
        Static method to validate fields in data.
        Optionally takes a list of specific fields to validate.
        Raises ValidationError if any required field is missing.
        """
        if fields is None:
            fields = data.keys()  # Validate all fields if no specific fields provided
        missing_fields = [field for field in fields if field not in data]
        if missing_fields:
            raise serializers.ValidationError({
                'detail': f"Fields {', '.join(missing_fields)} cannot be empty."
            })