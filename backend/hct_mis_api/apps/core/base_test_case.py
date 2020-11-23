import base64

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from elasticsearch_dsl import connections
from graphene.test import Client
from snapshottest.django import TestCase as SnapshotTestTestCase

from household.elasticsearch_utils import rebuild_search_index


class APITestCase(SnapshotTestTestCase):
    def setUp(self):
        from hct_mis_api.schema import schema

        super().setUp()
        self.client = Client(schema)

    def snapshot_graphql_request(self, request_string, context=None, variables=None):
        if context is None:
            context = {}

        graphql_request = self.client.execute(
            request_string, variables=variables, context=self.generate_context(**context),
        )

        self.assertMatchSnapshot(graphql_request)

    def graphql_request(self, request_string, context=None, variables=None):
        if context is None:
            context = {}

        return self.client.execute(
            request_string, variables=variables, context=self.generate_context(**context),
        )

    def generate_context(self, user=None, files=None):
        request = RequestFactory()
        context_value = request.get("/api/graphql/")
        context_value.user = user or AnonymousUser()
        self.__set_context_files(context_value, files)
        return context_value

    @staticmethod
    def id_to_base64(id, name):
        return base64.b64encode(f"{name}:{str(id)}".encode("utf-8")).decode()

    @staticmethod
    def __set_context_files(context, files):
        if isinstance(files, dict):
            for name, file in files.items():
                context.FILES[name] = file


class BaseElasticSearchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        connections.create_connection(hosts=["elasticsearch_test:9200"], timeout=20)
        cls.rebuild_search_index()

    @classmethod
    def tearDownClass(cls):
        rebuild_search_index()
        super().tearDownClass()

    @classmethod
    def rebuild_search_index(cls):
        rebuild_search_index()
