from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    message = "Only customers are allowed to access this resource."

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            # and getattr(user, "is_customer", False)
            # and not getattr(user, "is_review", False)
            and user.is_customer()
            and not user.is_review()
        )


class IsReviewer(BasePermission):
    message = "Only reviewers are allowed to access this resource."

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            # and getattr(user, "is_review", False)
            # and not getattr(user, "is_customer", False)
            and user.is_review() # call the method 
            and not user.is_customer() 
        )



# This IsClaimOwner code cares about the relationship between you and the specific data you are touching.
class IsClaimOwner(BasePermission):
    message = "You do not have permission to access this claim."

    def has_object_permission(self, request, view, obj):
        # Only authenticated users can pass
        if not request.user or not request.user.is_authenticated:
            return False

        # obj is expected to be a Claim instance
        return obj.customer == request.user