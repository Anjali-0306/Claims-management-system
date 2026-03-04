from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from claims.api.permissions import IsReviewer,IsClaimOwner
from django.shortcuts import get_object_or_404
from claims.api.serializers import ClaimCreateSerializer,ClaimUpdateSerializer,ClaimSerializer
from claims.models import Claim
from claims.exceptions import InvalidClaimState

class ReviewerClaimListView(APIView):
    permission_classes = [IsAuthenticated, IsReviewer]

    def get(self, request):
        claims = Claim.objects.filter(status=Claim.Status.SUBMITTED)
        data = [{"id": c.id, "customer": c.customer_id} for c in claims]
        return Response(data)



# Approve / Reject
class ReviewerApproveClaimView(APIView):
    permission_classes = [IsAuthenticated, IsReviewer]

    def post(self, request, pk):
        claim = Claim.objects.get(pk=pk)

        try:
            claim.approve(request.user)
        except InvalidClaimState as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response({"message": "Approved"})


class ReviewerRejectClaimView(APIView):
    permission_classes = [IsAuthenticated, IsReviewer]

    def post(self, request, pk):
        claim = Claim.objects.get(pk=pk)

        try:
            claim.reject(request.user)
        except InvalidClaimState as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response({"message": "Rejected"})
