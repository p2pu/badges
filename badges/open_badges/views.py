# Create your views here.
from django.http import HttpResponse
import json
from .helpers import reverse_url
from .helpers import static_url

def test(request):
    return HttpResponse('nekaj')


def get_assertion(request, uid):

    TEST_ASSERTION = {
        "uid": uid,
        "recipient": {
            "type": "email",
            "hashed": True,
            "salt": "deadsea",
            "identity": "sha256$c7ef86405ba71b85acd8e2e95166c4b111448089f2e1599f42fe1bba46e865c5"
        },
        "image": static_url('images/super-blogger_2.png'),
        "evidence": "https://example.org/beths-robot-work.html",
        "issuedOn": 1359217910,
        "badge": reverse_url('ob_get_badge', args=['9999']),
        "verify": {
            "type": "hosted",
            "url": reverse_url('ob_get_assertion', args=[uid])
        }
    }
    return HttpResponse(json.dumps(TEST_ASSERTION), mimetype="application/json")


def get_badge(request, badge_id):
    TEST_BADGE = {
        "name": "Awesome Robotics Badge",
        "description": "For doing awesome things with robots that people think is pretty great.",
        "image": static_url('images/super-blogger_2.png'),
        "criteria": "https://example.org/robotics-badge.html",
        "tags": ["robots", "awesome"],
        "issuer": reverse_url('ob_get_organisation'),
        "alignment": [
            { "name": "CCSS.ELA-Literacy.RST.11-12.3",
              "url": "http://www.corestandards.org/ELA-Literacy/RST/11-12/3",
              "description": "Follow precisely a complex multistep procedure when carrying out experiments, taking measurements, or performing technical tasks; analyze the specific results based on explanations in the text."
            },
            { "name": "CCSS.ELA-Literacy.RST.11-12.9",
              "url": "http://www.corestandards.org/ELA-Literacy/RST/11-12/9",
              "description": " Synthesize information from a range of sources (e.g., texts, experiments, simulations) into a coherent understanding of a process, phenomenon, or concept, resolving conflicting information when possible."
            }
        ]
    }
    return HttpResponse(json.dumps(TEST_BADGE), mimetype="application/json")


def get_organisation(request):
    TEST_ORGANISATION = {
        "name": "P2PU",
        "url": "https://www.p2pu.org",
    }
    return HttpResponse(json.dumps(TEST_ORGANISATION), mimetype="application/json")