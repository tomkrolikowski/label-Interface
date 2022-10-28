from django.shortcuts import render

from .forms import ContactForm
from .forms import UserForm
import os, random

# def set_globvar_to_one():
#     global globvar    # Needed to modify global copy of globvar
#     globvar = 1

def index(request):
    global count
    global first_time
    folder = 'rgb/'
    annotated_dir = 'annotated/'
    save_path = "labels/"
    if request.method == "POST":
        form = None
        if first_time == True:
            first_time = False
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                name = user_form.cleaned_data['user_name']
            else:
                name = "blank"
            # create a new label and image and save go to that page
            form = ContactForm()
            _, _, files = next(os.walk(save_path))
            total_count = len(files)
            a=random.choice(os.listdir(folder))
            form.Meta.model.photo_name = save_path + os.path.splitext(a)[0]
            image = folder + a
            annotated = annotated_dir + a
            context = {'form' : form, 'image' : image, 'annotated': annotated, 
                    'count' : count, "total" : total_count, 'name' : name}
            return render(request, 'index.html', context)
        
        else:
            form = ContactForm(request.POST)
            if len(form.errors) > 0:
                base_name = os.path.basename(form.Meta.model.photo_name) + '.jpg'
                _, _, files = next(os.walk(save_path))
                total_count = len(files)
                image = folder + base_name
                annotated = annotated_dir + base_name
                context = {'form' : form, 'image' : image, 'annotated': annotated, 
                        'count' : count, "total" : total_count }
                return render(request, 'index.html', context)
            if form.is_valid():
                # process the form associated with an image and save it as a numpy file
                base_name = os.path.basename(form.Meta.model.photo_name)
                if base_name != "":
                    os.remove(folder + base_name + ".jpg")
                    # form.Meta.model.user_name = name
                    form.save()
                    count += 1   
                
                # create a new label and image and save go to that page
                form = ContactForm()
                _, _, files = next(os.walk(save_path))
                total_count = len(files)
                a=random.choice(os.listdir(folder))
                form.Meta.model.photo_name = save_path + os.path.splitext(a)[0]
                image = folder + a
                annotated = annotated_dir + a
                context = {'form' : form, 'image' : image, 'annotated': annotated, 
                        'count' : count, "total" : total_count }
                return render(request, 'index.html', context)
        
    count = 0
    name = 'blank'
    user_form = UserForm()
    # form = ContactForm()
    a=random.choice(os.listdir(folder))
    first_time = True
    user_form.Meta.model.photo_name = save_path + os.path.splitext(a)[0]
    context = {'form' : user_form }
    return render(request, 'home.html', context)