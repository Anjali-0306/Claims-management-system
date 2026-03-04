from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from claims.api.permissions import IsCustomer,IsClaimOwner
from django.shortcuts import get_object_or_404
from claims.api.serializers import ClaimCreateSerializer,ClaimUpdateSerializer,ClaimSerializer
from claims.models import Claim
from claims.exceptions import InvalidClaimState




class CustomerClaimCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = ClaimCreateSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        claim = serializer.save(customer=request.user)

        return Response(
            {
                "id": claim.id,
                "status": claim.status,
                "message": "Claim created successfully",
            },
            status=status.HTTP_201_CREATED,
        )



# Update Draft Claim (PATCH)
class CustomerClaimUpdateView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsCustomer,
        IsClaimOwner,
    ]

    def patch(self, request, pk):
        claim = Claim.objects.get(pk=pk)
        self.check_object_permissions(request, claim)

        serializer = ClaimUpdateSerializer(
            claim,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        try:
            claim.update_draft(**serializer.validated_data)
        except InvalidClaimState as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response({"message": "Updated"})


# List Claims
class CustomerClaimListView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        claims = Claim.objects.filter(customer=request.user)
        # data = [{"id": c.id, "status": c.status} for c in claims]
        data = ClaimSerializer(claims, many=True).data
        return Response(data)





# Update Submit Claim (PATCH)
class CustomerClaimSubmitView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsCustomer,
        IsClaimOwner,
    ]

    def post(self, request, pk):
        claim = Claim.objects.get(pk=pk)
        self.check_object_permissions(request, claim)

        try:
            claim.submit(request.user)
        except InvalidClaimState as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response({"message": "Submitted"})
