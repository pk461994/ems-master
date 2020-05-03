from rest_framework import serializers

from poll.models import Question, Choice, Tag
from employee.serializers import EmployeeSerializer


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choice
        fields = [
            'id',
            'question',
            'text'
        ]
        read_only_fields = ('question',)
        # depth = 2


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "title",
            "status",
            "created_by",
            "choices",
            "tags"
        ]
        read_only_fields = ["tags"]

    def create(self, validated_data):
       choices = validated_data.pop('choices')
       question = Question.objects.create(**validated_data)
       return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices')
        print('choices are', choices)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        keep_choices = []
        existing_ids = [c.id for c in instance.choices]
        for choice in choices:
            if 'id' in choice.keys():
                if Choice.objects.filter(id = choice['id']).exists():
                    c = Choice.objects.get(id = choice['id'])
                    c.text = choice.get('text', c.text)
                    c.save()
                    keep_choices.append(c.id)
                else:
                    continue
            else:
                c = Choice.objects.create(**choice, question=instance)
                keep_choices.append(c.id)

        for choice in instance.choices:
            if choice.id not in keep_choices:
                choice.delete()
        
        return instance #Returning Question after successful operations

class PollSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    status = serializers.CharField()
    created_by = EmployeeSerializer()
    created_at = serializers.DateTimeField()

    class Meta:
        model = Question