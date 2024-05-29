import json

from rest_framework.renderers import JSONRenderer


# for detaileview
class QuestionJSONRenderer(JSONRenderer):
    """Defalut renderer class for single Question object."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        # in case of DELETE request, the "data" will be None else "data" will hold queryset or error codes
        # although there will be no DELETE request. logic applied for sanity.
        if data is not None:
            errors = data.get("errors", None)
        else:
            errors = None
        # if there are errors, then render as per default JSON style. Pass if errors is None
        if errors is not None:
            return super(QuestionJSONRenderer, self).render(data)
        else:
            return json.dumps({"status_code": status_code, "question": data})


# for questions => *s (listview)
class QuestionsJSONRenderer(JSONRenderer):
    """Defalut renderer class for single Question object."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        errors = data.get("errors", None)

        # if there are errors, then render as per default JSON style. Pass if errors is None
        if errors is not None:
            return super(QuestionJSONRenderer, self).render(data)
        else:
            return json.dumps({"status_code": status_code, "questions": data})
