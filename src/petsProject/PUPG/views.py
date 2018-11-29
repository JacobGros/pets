import random
from PUPG.models import Person, Pet
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from PUPG.forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

# Create your views here.
def index(request):

    num_pets = Pet.objects.all().count()
    num_people = Person.objects.all().count()


    ordered_pets = []

    for pet in Pet.objects.all().order_by('-vote_count'):
        ordered_pets.append(pet)

    

    context = {
            "num_pets": num_pets,
            "num_people": num_people,
            "winner": ordered_pets[0],
            "random pet": ordered_pets[random.randint(0,(num_pets-1))]
            }



    if request.user.is_authenticated:
        user = request.user
        person = user.person
        context["person"] = person


    return render(request, "index.html", context=context)

@login_required
def vote(request):

    user = request.user

    num_pets = Pet.objects.all().count()
    num_people = Person.objects.all().count()
    
    x = random.randint(0, Pet.objects.all().count()-1)
    
    
    contender1 =  Pet.objects.all()[x]

    while(contender1.pet_owner == user.person):
        x = random.randint(0, Pet.objects.all().count()-1)
        contender1 =  Pet.objects.all()[x]

    
    x = random.randint(0, Pet.objects.all().count()-1)

    contender2 =  Pet.objects.all()[x]


    while (contender1 == contender2 or contender2.pet_owner == user.person):
        
        x = random.randint(0, Pet.objects.all().count()-1)
        contender2 =  Pet.objects.all()[x]


    

    context = {
                "c1": contender1,
                "c2": contender2,
                }





    if request.user.is_authenticated:
        user = request.user
        person = user.person
        context["person"] = person

    return render(request, "versus.html", context=context)

def vote_for_pet(request, id):
    pet = Pet.objects.get(id=id)
    pet.vote_count += 1
    pet.save()
    return HttpResponseRedirect('/PUPG/vote/')


def leaderboard(request):
    num_pets = Pet.objects.all().count()

    ordered_pets = []

    context = {
                "num_pets": num_pets,
                }

    
    for pet in Pet.objects.all().order_by('-vote_count'):
        ordered_pets.append(pet)
    context["ordered_pets"] = ordered_pets 



    if request.user.is_authenticated:
        user = request.user
        person = user.person
        context["person"] = person

    return render(request, "leaderBoardDraft1.html", context=context)


class PetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pet
    template_name = "submit.html"
    fields = ['name', 'age', 'animal_type', 'picture']
    #fields = '__all__'
    
    

    def form_valid(self, form):
        form.instance.pet_owner = self.request.user.person
        form.instance.vote_count = '0'
        return super(PetCreateView, self).form_valid(form)

class PersonDetailView(generic.DetailView):
    model = Person
    template_name = "person_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = [] 
        profile_votes = 0
        for pet in Pet.objects.all().filter(pet_owner = context['object']):
            pets.append(pet)
            profile_votes = profile_votes + pet.vote_count

        context['pets'] = pets
        context['votes'] = profile_votes
        return context 



class PetDetailView(generic.DetailView):
    model = Pet
    template_name = "pet_detail.html"

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
             user = form.save()
             user.refresh_from_db()
             user.person.name = form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name')
             user.save()
             raw_password = form.cleaned_data.get('password1')
             user = authenticate(username=user.username, password=raw_password)
             login(request, user)
             return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form': form})

