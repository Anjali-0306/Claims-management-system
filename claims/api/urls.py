from django.urls import path

from claims.api.views.customer import (
    CustomerClaimCreateView,
    CustomerClaimListView,
    CustomerClaimUpdateView,
    CustomerClaimSubmitView,
)

from claims.api.views.reviewer import (
    ReviewerClaimListView,
    ReviewerApproveClaimView,
    ReviewerRejectClaimView,
)

urlpatterns = [
    # --------------------
    # Customer endpoints
    # --------------------
    path(
        "customer/claims/",
        CustomerClaimListView.as_view(),
        name="customer-claim-list",
    ),
    path(
        "customer/claims/create/",
        CustomerClaimCreateView.as_view(),
        name="customer-claim-create",
    ),
    path(
        "customer/claims/<int:pk>/",
        CustomerClaimUpdateView.as_view(),
        name="customer-claim-update",
    ),
    path(
        "customer/claims/<int:pk>/submit/",
        CustomerClaimSubmitView.as_view(),
        name="customer-claim-submit",
    ),

    # --------------------
    # Reviewer endpoints
    # --------------------
    path(
        "reviewer/claims/",
        ReviewerClaimListView.as_view(),
        name="reviewer-claim-list",
    ),
    path(
        "reviewer/claims/<int:pk>/approve/",
        ReviewerApproveClaimView.as_view(),
        name="reviewer-claim-approve",
    ),
    path(
        "reviewer/claims/<int:pk>/reject/",
        ReviewerRejectClaimView.as_view(),
        name="reviewer-claim-reject",
    ),
]
