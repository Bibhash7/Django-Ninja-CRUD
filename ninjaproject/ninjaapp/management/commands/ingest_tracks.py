from datetime import datetime
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from ninjaapp.models import Track

class Command(BaseCommand):
    help = 'Create tracks from JSON file'

    def handle(self, *args, **kwargs):
        # set the path to the datafile
        datafile = settings.BASE_DIR / 'data' / 'tracks.json'
        assert datafile.exists()

        # load the datafile
        with open(datafile, 'r') as f:
            data = json.load(f)
        
        # create tz-aware datetime object from the JSON string.
        DATE_FMT = "%Y-%m-%d %H:%M:%S"
        for track in data:
            track_date = datetime.strptime(track['last_play'], DATE_FMT)
            track['last_play'] = make_aware(track_date)

        # convert list of dictionaries to list of Track models, and bulk_create
        tracks = [Track(**track) for track in data]

        Track.objects.bulk_create(tracks)