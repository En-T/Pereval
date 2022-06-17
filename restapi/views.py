import json
from .models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@csrf_exempt
def submitData(request):  
    try:
        data = json.loads(request.POST['json'])
        if User.objects.filter(email=data['user']['email']):
            user = User.objects.get(email=data['user']['email']).pk
        else:
            user = add_user(data['user'])
        coords = add_coords(data['coords'])
        images = add_images(data['images'])
        pereval = add_pereval(data['beauty_title'], 
                         data['title'], 
                         data['other_titles'], 
                         data['connect'], 
                         data['level'], 
                         user, 
                         coords
                        )
        add_pereval_images(images, pereval)
    except:
        return HttpResponse(content='Bad Request', status=400)
    
    return HttpResponse(content=f'Успех, id = {pereval}', status=200)


def get_submitData_email(_, email):
    try:
        pereval = []
        user = User.objects.get(email=email)        
        perevals = Pereval.objects.filter(Q(user=user.pk) & Q(status='n'))
        for prvl in perevals:
            pereval.append(get_pereval(prvl.pk))
    except:
        return HttpResponse(content='Bad Request', status=400)
    return HttpResponse(content=pereval, status=200)


def get_submitData_id(_, pk):    
    try:         
        pereval = get_pereval(pk)
    except:
        return HttpResponse(content='Bad Request', status=400)
    return HttpResponse(content=pereval, status=200)

@csrf_exempt
def patch_submitData_id(request, pk): 
    try:   
        data = json.loads(request.POST['json'])     
        pereval = Pereval.objects.get(Q(pk=pk) & Q(status='n'))
        pereval.beauty_title = data['beauty_title'] 
        pereval.title = data['title'] 
        pereval.other_titles = data['other_titles'] 
        pereval.connect = data['connect'] 
        pereval.l_winter = data['level']['winter'] 
        pereval.l_summer = data['level']['summer']
        pereval.l_autumn = data['level']['autumn']
        pereval.l_spring = data['level']['spring']
        coords = Coords.objects.get(pk=pereval.coords.pk)
        coords.latitude= data['coords']['latitude']
        coords.longtude = data['coords']['longitude']
        coords.height = data['coords']['height']
        images = Pereval_Images.objects.filter(pereval=pereval.coords.pk)
        for i, img in enumerate(images):                               
            image = Images.objects.get(pk=img.images.pk) 
            image.data = data['images'][i]['data']
            image.title = data['images'][i]['title']
            image.save()            
        pereval.save()
        coords.save()
    except:
        return HttpResponse(content='state: 0', status=400)
    return HttpResponse(content='state: 1', status=200)


def add_pereval(beauty_title, title, other_titles, connect, level, user, coords):
    pereval = Pereval.objects.create(beauty_title=beauty_title, 
                                    title=title, 
                                    other_titles=other_titles, 
                                    connect=connect, 
                                    l_winter=level['winter'], 
                                    l_summer=level['summer'],
                                    l_autumn=level['autumn'],
                                    l_spring=level['spring'],
                                    coords_id=coords,
                                    user_id=user
                                    )
    return pereval.id

def add_user(user):
    name =user['fam'] + ' ' + user['name'] + ' ' + user['otc']    
    user = User.objects.create(name=name, email=user['email'], phone=user['phone'])
    return user.id

def add_coords(coords):
    coords = Coords.objects.create(latitude=coords['latitude'],longtude=coords['longitude'],height=coords['height'])
    return coords.id

def add_images(images):
    img = []
    for image in images:        
        images = Images.objects.create(data=image['data'], title=image['title'])
        img.append(images.id)
    return img

def add_pereval_images(images,pereval):
    for img in images:
        Pereval_Images.objects.create(images_id=img, pereval_id=pereval)


def get_pereval(pk):
    pereval = Pereval.objects.get(pk=pk)
    images = get_images(pk)
    json = { "beauty_title": pereval.beauty_title,
                "title": pereval.title,
                "other_titles": pereval.other_titles,
                "connect": pereval.connect, 
                "status": pereval.status, 
                "user": {"email": pereval.user.email, 		
                        "name": pereval.user.name,
                        "phone": pereval.user.phone}, 
                
                "coords":{
                "latitude": pereval.coords.latitude,
                "longitude": pereval.coords.longtude,
                "height": pereval.coords.height},                
                
                "level":{
                "winter": pereval.l_winter, 
                "summer": pereval.l_summer,
                "autumn": pereval.l_autumn,
                "spring": pereval.l_spring},
                
                "images":
                    images
            }    
    return str(json)

def get_images(pk):
    all_images = []
    images = {}
    pereval = Pereval_Images.objects.filter(pereval=pk)    
    for image in pereval:
        img = Images.objects.filter(pk=image.pk)
        for i in img:
            images['data'] = i.data
            images['title'] = i.title
            all_images.append(images)
    return all_images
    