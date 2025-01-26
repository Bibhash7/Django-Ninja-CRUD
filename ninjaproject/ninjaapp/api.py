from typing import List
from ninja import NinjaAPI
from pydantic import ValidationError
from ninjaapp.schema import TrackSchema, ErrorSchema, SuccessSchema
from ninjaapp.models import Track
from ninjaapp.constants import SuccessMessage, ErrorMessage

app = NinjaAPI()




@app.get('test/')
def test(request):
    return 200, {'test':'success'}

@app.get('tracks/', response=SuccessSchema)
def get_tracks(request):
    return {SuccessMessage.Success: list(Track.objects.all().values('title'))}

@app.get(
    'tracks/{track_id}', 
    response={200: SuccessSchema, 404: ErrorSchema, 500: ErrorSchema, 422: ErrorSchema}
)
def get_single_track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        return track
    except OverflowError:
        return 500, {ErrorMessage.Error: ErrorMessage.OVERFLOW}
    except Track.DoesNotExist:
        return 404, {ErrorMessage.Error: ErrorMessage.DOES_NOT_EXIST}
    
@app.get(
    'track_filter/{title}', 
    response={200: SuccessSchema, 404: ErrorSchema, 500: ErrorSchema, 422: ErrorSchema}
)
def get_track_by_title(request, title: str):
    try:
        track = Track.objects.filter(title__icontains=title)
        return 200, {SuccessMessage.Success: track}
    except Exception as error:
        return 500, {ErrorMessage.Error: ErrorMessage.INTERNAL_SERVER_ERROR}
    
    
@app.post(
    'create-track/',
    response={200: TrackSchema, 500: ErrorSchema}
)
def create_track(request, track: TrackSchema):
    try:
        track = Track.objects.create(**track.dict())
        return 200, track
    except Exception as error:
        return 500, {ErrorMessage.Error: ErrorMessage.INTERNAL_SERVER_ERROR} 
    
@app.put(
    'update-track/{track_id}',
    response={200: TrackSchema, 404: ErrorSchema, 500: ErrorSchema}    
)   
def update_track(request, track_id: int, data: TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attr, value in data.dict().items():
            setattr(track, attr, value)
            track.save()
        return 200, track
    except Track.DoesNotExist:
        return 404, {ErrorMessage.Error: ErrorMessage.DOES_NOT_EXIST}
    except Exception as error:
        return 500, {ErrorMessage.Error: ErrorMessage.INTERNAL_SERVER_ERROR} 
        

    

