from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .forms import VacancyForm


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def vacancy_view(request):
    form = VacancyForm(request.data, request.FILES)

    if form.is_valid():
        vacancy = form.save()
        return Response(
            {"message": "Резюме успешно отправлено", "id": vacancy.id},
            status=status.HTTP_200_OK,
        )

    return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)
