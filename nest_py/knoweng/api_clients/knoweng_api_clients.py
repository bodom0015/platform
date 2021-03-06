import nest_py.knoweng.data_types.knoweng_schemas as knoweng_schemas
import nest_py.core.api_clients.smoke_scripts as smoke_scripts
from nest_py.core.api_clients.smoke_scripts import SmokeTestResult
from nest_py.core.api_clients.tablelike_api_client_maker import TablelikeApiClientMaker
from nest_py.knoweng.api_clients.jobs_api_client import JobsApiClientMaker
from nest_py.knoweng.api_clients.files_api_client import FilesApiClientMaker

def get_api_client_makers():
    client_makers = dict()

    jobs_cm = JobsApiClientMaker()
    client_makers[jobs_cm.get_collection_name()] = jobs_cm

    files_cm = FilesApiClientMaker()
    client_makers[files_cm.get_collection_name()] = files_cm

    schemas = knoweng_schemas.get_schemas().values()
    for schema in schemas:
        name = schema.get_name()
        #the nonstandard clients were added above, and will already have
        #an entry that we don't want to override
        if not name in client_makers:
            cm = TablelikeApiClientMaker(schema)
            client_makers[name] = cm
    return client_makers

def run_all_smoke_tests(http_client):
    smoke_res = SmokeTestResult('knoweng')
    acm_registry = get_api_client_makers()
    smoke_scripts.login_client(http_client, smoke_res)
    for ep_name in acm_registry:
#    for ep_name in ['files']:
        acm = acm_registry[ep_name]
        acm.run_smoke_scripts(http_client, smoke_res)
    return smoke_res

