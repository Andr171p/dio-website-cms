from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .forms import VacancyForm


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def vacancy_view(request) -> Response:
    form_data = {
        "title": request.data.get("title"),
        "name": request.data.get("name"),
        "phone": request.data.get("phone"),
    }

    # Создаем форму с данными и файлом
    form = VacancyForm(form_data, request.FILES)
    if form.is_valid():
        form.save()
        return Response(status=status.HTTP_200_OK)
    return Response(
        status=status.HTTP_400_BAD_REQUEST,
    )
