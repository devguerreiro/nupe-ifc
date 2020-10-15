from nupe.core.serializers.attendance import (
    AttendanceCreateSerializer,
    AttendanceDetailSerializer,
    AttendanceListSerializer,
)
from nupe.core.serializers.course import (
    AcademicEducationDetailSerializer,
    AcademicEducationSerializer,
    GradeSerializer,
)
from nupe.core.serializers.institution import (
    CampusCreateSerializer,
    CampusDetailSerializer,
    CampusListSerializer,
    InstitutionSerializer,
)
from nupe.core.serializers.job import FunctionSerializer, SectorSerializer
from nupe.core.serializers.location import CitySerializer, LocationSerializer, StateSerializer
from nupe.core.serializers.person import PersonCreateSerializer, PersonDetailSerializer, PersonListSerializer
from nupe.core.serializers.reason import AttendanceReasonSerializer
from nupe.core.serializers.student import StudentCreateSerializer, StudentDetailSerializer, StudentListSerializer
