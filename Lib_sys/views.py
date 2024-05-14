from django.shortcuts import render, redirect
import os
from django.conf import settings
from .models import *
from .forms import *
from datetime import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
import barcode
import barcode.writer
from barcode.writer import ImageWriter, SVGWriter
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

@login_required
def home(request):
    clients = Client.objects.count()
    livres = Bouquin.objects.count()
    exemplaires = Exemplaire.objects.count()
    emprunts = Emprunt.objects.filter(Retourne="-").count()
    return render(request, 'index.html', {'Clients': clients, 'Livres': livres, 'Exemplaires': exemplaires, 'Emprunts': emprunts})

def user_login(request):
    msg = ""
    if request.method == "POST":
        usern = request.POST["username"]
        passw = request.POST["password"]

        user = authenticate(request, username=usern, password=passw)
        
        if user is not None:
            login(request, user)
            next_page = request.POST.get('next', 'home')
            return redirect('home') 
            
        else:
            msg = "Wrong Username or password !"
    return render(request, "login.html", {'msg': msg})

def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
def clients(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, initial={'status': 'Active'})
        if form.is_valid():
            client = form.save()
            # Generating CodeBar for new client
            client_id = client.id
            code128_class = barcode.get_barcode_class('code128')
            barcode_instance = code128_class(str(client_id), writer=ImageWriter())
            file_path = os.path.join(settings.STATIC_ROOT, 'IDS', f'user_{client_id}')
            barcode_instance.save(file_path, options={'module_width': 0.5, 'module_height': 20, 'quiet_zone': 1})
            return redirect('Clients')
    else:
        form = ClientForm(initial={'status': 'Active'})
    
    return render(request, 'Clients.html', {'clients': clients, 'form': form})

@login_required
def delete_client(request, id):
    user = Client.objects.get(pk=id)
    # Delete Codebar
    file_path = os.path.join(settings.STATIC_ROOT, 'IDS', f'user_{id}.png')
    if os.path.exists(file_path):
        os.remove(file_path)
        
    user.delete()
    return redirect('Clients')

@login_required
def edit_client(request, id):
    user = Client.objects.get(pk=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('Clients')
    else:
        form = ClientForm(instance=user)
    return render(request, 'Client.html', {'form': form, 'client': user})

@login_required
def actdes(request, id):
    user = Client.objects.get(pk=id)
    action = request.GET.get("action")
    if action == "act": 
        user.activer()
    else:
        user.desactiver()

    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
def livres(request):
    livres = Bouquin.objects.all()
    if request.method == "POST": 
        form = LivresForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = LivresForm()

    return render(request, 'Livres.html', {'livres': livres, 'form': form})

@login_required
def livre(request, ISBN):
    livre = Bouquin.objects.get(ISBN=ISBN)
    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('Livres')
    else:
        form = LivreForm(instance=livre)

    return render(request, 'Livre.html', {'livre': livre, 'form': form})

@login_required
def delete_livre(request, id):
    livre = Bouquin.objects.get(pk=id)
    livre.delete()

    return redirect("Livres")

@login_required
def emprunt_client(request, id):
    client = Client.objects.get(pk=id)
    emp = Emprunt.objects.filter(Client=client, Retourne="-")
    ids = [em.Exemplaire.Bouquin.id for em in emp]
    livres = Bouquin.objects.filter(Statut="Disponible pour prêt").exclude(id__in=ids).values()
    count = Emprunt.objects.filter(Client=client, Retourne="-").count()

    return render(request, 'rent_u.html', {'livres': livres, 'client': client, 'count': count})

@login_required
def emprunt_livre(request, id):
    clients = Client.objects.filter(Statut="Active")
    livre = Bouquin.objects.get(pk=id)
    exemplaire = Exemplaire.objects.filter(Bouquin=livre, Statut='Disponible').last()
    
    return render(request, 'rent_liv.html', {'livre': livre, 'exemplaire': exemplaire, 'clients': clients})

@login_required
def emprunt(request, id):
    
    livre = Bouquin.objects.get(pk=id)
    exemplaire = Exemplaire.objects.filter(Bouquin=livre, Statut='Disponible').last()
    client = Client.objects.get(id=request.POST.get("client"))
    page_prec = "Clients"
    date_r = datetime.now() + timedelta(weeks=2)
    
    Emprunt.objects.create(
                Exemplaire=exemplaire,
                Client=client,
                bibliothecaire=request.user,
                Date_retour=date_r
            )
    exemplaire.emprunt_exmp()
    return redirect(page_prec)

@login_required
def emps_hist(request):
    emps = Emprunt.objects.all()
    c_date = datetime.today().date()
    #Quand un exemplaire prêté ne revient pas à la bibliothèque
    emps_p = Emprunt.objects.filter(Date_retour__lt=c_date, Retourne='-')
    for emp in emps_p:
        #il est considéré comme perdu
        emp.perdu()
    #aprés un an
    emps_p_an = Emprunt.objects.filter(Date_retour__lt=c_date-timedelta(days=365), Retourne='Perdu')
    for emp in emps_p_an:
        #on la retirer de la base 
        emp.delete()
    return render(request, 'emprunt_hist.html', {'emps': emps})

@login_required
def return_emp(request, id):
    emp = Emprunt.objects.get(pk=id)
    act = request.GET.get("act")
    emp.return_exmp(act)
    return redirect('Emprunt_hist')

@login_required
def exemplaires(request):
    exmps = Exemplaire.objects.all()
    return render(request, 'Exemplaires.html', {'exemplaires': exmps})

@login_required
def pret(request, id):
    livre = Bouquin.objects.get(pk=id)
    pret = request.GET.get("pret") 
    livre.prett(pret)
    exemplaires = Exemplaire.objects.filter(Bouquin=livre, Statut="Disponible")
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
def modifier_exmp(request, id):
    ob = Exemplaire.objects.get(pk=id)
    if request.GET.get("act") == "renv":
        ob.renouvler()
    else:
        ob.retirer()
    return redirect("Exemplaires")

def acheter_plus(request, id):
    livre = Bouquin.objects.get(pk=id)
    n = int(request.POST.get("n_plus"))
    for i in range(livre.Quantite_achete, livre.Quantite_achete+n):
        Exemplaire.objects.create(
            Bouquin=livre,
            Id_exemplaire=f"{livre.ISBN}-{i + 1}"
        )
    livre.Quantite_achete += n
    livre.save()

    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

