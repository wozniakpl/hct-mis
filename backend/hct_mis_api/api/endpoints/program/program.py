from rest_framework import serializers
from rest_framework.generics import ListAPIView

from hct_mis_api.api.endpoints.base import HOPEAPIView
from hct_mis_api.apps.program.models import Program


class ProgramGlobalSerializer(serializers.ModelSerializer):
    business_area_code = serializers.CharField(source="business_area.code", read_only=True)

    class Meta:
        model = Program
        fields = (
            "id",
            "name",
            "programme_code",
            "status",
            "start_date",
            "end_date",
            "budget",
            "frequency_of_payments",
            "sector",
            "scope",
            "cash_plus",
            "population_goal",
            "business_area_code",
        )


class ProgramGlobalListView(HOPEAPIView, ListAPIView):
    serializer_class = ProgramGlobalSerializer
    queryset = Program.objects.all()
