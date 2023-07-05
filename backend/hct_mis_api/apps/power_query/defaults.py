from typing import Any, Dict

from django.contrib.contenttypes.models import ContentType

from hct_mis_api.apps.account.models import Partner, User
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.models import Household

SYSTEM_PARAMETRIZER: Dict[str, Dict[str, Any]] = {
    "active-business-areas": {
        "name": "Active Business Areas",
        "value": lambda: {
            "business_area": list(BusinessArea.objects.filter(active=True).values_list("slug", flat=True))
        },
    },
    "all-partners": {
        "name": "All Partners",
        "value": lambda: {"partner": list(Partner.objects.values_list("name", flat=True))},
    },
}


def create_defaults() -> None:
    if User.objects.filter(is_superuser=True).first() is None:
        return
    from hct_mis_api.apps.power_query.models import Formatter, Parametrizer

    fmt_html, __ = Formatter.objects.get_or_create(
        name="Dataset To HTML",
        defaults={
            "code": """
<h1>{{title}}</h1>
<table>
    <tr>{% for fname in dataset.data.headers %}<th>{{ fname }}</th>{% endfor %}</tr>
{% for row in dataset.data %}<tr>{% for col in row %}<td>{{ col }}</td>{% endfor %}</tr>
{% endfor %}
    </table>
"""
        },
    )

    Formatter.objects.get_or_create(
        name="Queryset To HTML",
        defaults={
            "code": """
<h1>{{title}}</h1>
<table>
    <tr><th>id</th><th>str</th></tr>
{% for row in dataset.data %}<tr>
    <td>{{ row.id }}</td>
    <td>{{ row }}</td>
    </tr>
{% endfor %}
    </table>
""",
            "content_type": "html",
        },
    )

    Formatter.objects.get_or_create(name="Dataset To XLS", defaults={"code": "", "content_type": "xls"})

    for code, params in SYSTEM_PARAMETRIZER.items():
        Parametrizer.objects.update_or_create(
            name=params["name"], code=code, defaults={"system": True, "value": params["value"]()}
        )
    from hct_mis_api.apps.power_query.models import Query, Report

    q, __ = Query.objects.update_or_create(
        name="Households by BusinessArea",
        defaults=dict(
            target=ContentType.objects.get_for_model(Household),
            code="""ba=BusinessAreaManager.get(slug=args['business_area'])
result=conn.filter(business_area=ba)
extra={"ba": ba}
""",
            parametrizer=Parametrizer.objects.get(code="active-business-areas"),
            owner=User.objects.filter(is_superuser=True).first(),
        ),
    )

    Report.objects.update_or_create(
        name="Household by BusinessArea",
        defaults={"query": q, "formatter": fmt_html, "document_title": "Household by BusinessArea: %(business_area)s"},
    )
