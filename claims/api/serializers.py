from rest_framework import serializers
from claims.models import Claim 

class ClaimCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['policy','description']

    def validate_policy(self,policy):
        user = self.context["request"].user

        if policy.customer != user:
            raise serializers.ValidationError("Invalid Policy")

        if not policy.is_active:
            raise serializers.ValidationError("Policy inactive")

        return policy


class ClaimUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ["description"]


#test
class ClaimSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Claim 
        fields = "__all__"

