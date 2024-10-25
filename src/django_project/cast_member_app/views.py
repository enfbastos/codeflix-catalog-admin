from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from src.core.cast_member.application.create_cast_member import (
    CreateCastMember, CreateCastMemberInput)
from src.core.cast_member.application.delete_cast_member import (
    DeleteCastMember, DeleteCastMemberInput)
from src.core.cast_member.application.exceptions import (CastMemberNotFound,
                                                         InvalidCastMember)
from src.core.cast_member.application.list_cast_member import (
    ListCastMember, ListCastMemberInput)
from src.core.cast_member.application.update_cast_member import (
    UpdateCastMember, UpdateCastMemberInput)
from src.django_project.cast_member_app.repository import \
    DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer, CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer, ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input=ListCastMemberInput()
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())        
        output = use_case.execute(input)
        response_serializer = ListCastMemberResponseSerializer(output)
        return Response(status=HTTP_200_OK, data=response_serializer.data)
    
    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input = CreateCastMemberInput(**serializer.validated_data)
        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            output = use_case.execute(input)
        except InvalidCastMember as error:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(error)})
        response_serializer = CreateCastMemberResponseSerializer(output)
        return Response(status=HTTP_201_CREATED, data=response_serializer.data)
        
    def update(self, request: Request, pk: UUID = None) -> Response:
        serializer = UpdateCastMemberRequestSerializer(data={**request.data, "id": pk})
        serializer.is_valid(raise_exception=True)
        input = UpdateCastMemberInput(**serializer.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except InvalidCastMember as error:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(error)})
        return Response(status=HTTP_204_NO_CONTENT)
        
    def destroy(self, request: Request, pk: UUID = None) -> Response:
        request_data = DeleteCastMemberRequestSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)
        input = DeleteCastMemberInput(**request_data.validated_data)
        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_204_NO_CONTENT)
