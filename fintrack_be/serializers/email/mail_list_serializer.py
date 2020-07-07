from rest_framework import serializers

from fintrack_be.models import EmailTemplate, MailList


class MailListSerializer(serializers.ModelSerializer):
    template = serializers.SlugRelatedField(many=False,
                                            read_only=False,
                                            queryset=EmailTemplate.objects.all(),
                                            slug_field='template_key')

    class Meta:
        model = MailList
        fields = ['id', 'name', 'description', 'template', 'send_time', 'send_days']


class MailListRecipientsSerializer(serializers.ModelSerializer):
    recipients = serializers.StringRelatedField(many=True)

    class Meta:
        model = MailList
        fields = ['id', 'name', 'recipients']
