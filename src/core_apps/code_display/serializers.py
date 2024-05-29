from rest_framework import serializers


from core_apps.code_display.models import Questions, Companies
from core_apps.code_result.models import CodeExecutionResult


class TaglistField(serializers.Field):
    """Get all the tags in a list form"""

    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tags.")

        all_tags = []
        for tag in data:
            # strip spaces from tag, if then tag is empty string, continue
            tag = tag.strip()
            if not tag:
                continue
            all_tags.append(tag)
        return all_tags


class CompanySerializer(serializers.ModelSerializer):
    """Company Model Serializer"""

    class Meta:
        model = Companies
        fields = ["id", "title", "description"]


class QuestionGETSerializer(serializers.ModelSerializer):
    """'Seiralizer for Question Model"""

    companies = CompanySerializer(
        many=True,
        read_only=True,
    )
    problem_number = serializers.IntegerField(source="pkid", read_only=True)
    question_image = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    tags = TaglistField()

    def get_question_image(self, obj):
        return obj.image.url if obj.image.url else None

    def get_created_at(self, obj):
        created_date = obj.created_at
        formatted_date = created_date.strftime("%d/%m/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        updated_date = obj.updated_at
        formatted_date = updated_date.strftime("%d/%m/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        model = Questions
        fields = [
            "id",
            "problem_number",
            "title",
            "difficulty",
            "description",
            "testcases_example",
            "constraints",
            "acceptance_rate",
            "question_image",
            "tags",
            "companies",
            "created_at",
            "updated_at",
        ]


# the api will only be responsible for GET requests. POST/PUT will be handled from admin.
# as the api is read-only, no need for POST and PUT operations.
'''
class QuestionSerializer(serializers.ModelSerializer):
    """'Seiralizer for Question Model"""

    companies = CompanySerializer(
        many=True,
        read_only=True, 
        queryset=Companies.objects.all()
    )
    question_image = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    tags = TaglistField()

    def question_image(self, obj):
        return obj.image.url if obj.image.url else None 

    def get_created_at(self, obj):
        created_date = obj.created_at
        formatted_date = created_date.strftime("%d/%m/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        updated_date = obj.updated_at
        formatted_date = updated_date.strftime("%d/%m/%Y, %H:%M:%S")
        return formatted_date

    def create(self, validated_data):
        companies = validated_data.pop("companies", [])
        tags = validated_data.pop("tags", [])
        question = Questions.objects.create(**validated_data)
        question.tags.set(tags)
        question.companies.set(companies)
        question.save()
        return question

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.difficulty = validated_data.get("difficulty", instance.difficulty)
        instance.description = validated_data.get("description", instance.deccription)
        instance.test_cases = validated_data.get("test_cases", instance.test_cases)
        instance.examples = validated_data.get("examples", instance.examples)
        instance.image = validated_data.get("image", instance.image)
        instance.constrains = validated_data.get("constraints", instance.constrains)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        if "companies" in validated_data:
            instance.companies.set(validated_data.get("companies"))
        if "tags" in validated_data:
            instance.tags.set(validated_data.get("tags"))

        instance.save()
        return instance

    class Meta:
        model = Questions
        fields = [
            "id",
            "title",
            "difficulty",
            "description",
            "test_cases",
            "examples",
            "constraints",
            "tags",
            "companies",
            "created_at",
            "updated_at",
        ]


'''
