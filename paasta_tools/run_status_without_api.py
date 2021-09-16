import json
import time

from paasta_tools.api import api
from paasta_tools.instance import kubernetes as pik


api.setup_paasta_api()

start = time.time()
instance_status = pik.instance_status(
    service="mtb_ranking",
    instance="main",
    verbose=0,
    include_smartstack=True,
    include_envoy=True,
    use_new=True,
    instance_type="kubernetes",
    settings=api.settings,
)
end = time.time()
print(
    json.dumps(
        {"url": "everything", "start": start, "end": end, "duration": end - start}
    )
)
# print(instance_status)
