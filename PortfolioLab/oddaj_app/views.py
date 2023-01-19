from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from oddaj_app.forms import UserUpdateForm
from oddaj_app.models import Donations, Institution, Category, User
from django.core.paginator import Paginator


class LandingPage(View):
    def get(self, request):
        num_of_bags = Donations.objects.aggregate(Sum('quantity'))['quantity__sum']
        num_of_institutions = Donations.objects.aggregate(Count('institution'))['institution__count']
        page = request.GET.get('page')

        foundations = Institution.objects.filter(type="Fundacja")
        paginator_foundations = Paginator(foundations, 5)
        page_foundations = paginator_foundations.get_page(page)

        gov_organizations = Institution.objects.filter(type="Organizacja")
        paginator_organizations = Paginator(gov_organizations, 5)
        page_organizaitons = paginator_organizations.get_page(page)

        collections = Institution.objects.filter(type="Zbiorka")
        paginator_collections = Paginator(collections, 5)
        page_collections = paginator_collections.get_page(page)

        return render(request, 'index.html', {'bags': num_of_bags, 'institutions': num_of_institutions,
                                              "foundations": page_foundations,
                                              "gov_organizations": page_organizaitons,
                                              "collections": page_collections})


class AddDonation(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request):
        categories = Category.objects.all()
        organizations = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'organizations': organizations})

    def post(self, request):
        categories = request.POST.getlist("categories")
        bags = request.POST.get("bags")
        organization = request.POST.get("organization")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        date = request.POST.get("data")
        time = request.POST.get("time")
        more_info = request.POST.get("more_info")

        new_donation = Donations.objects.create(categories=categories,
                                                quantity=bags,
                                                institution=organization,
                                                address=address,
                                                city=city,
                                                zip_code=postcode,
                                                phone_number=phone,
                                                pick_up_date=date,
                                                pick_up_time=time,
                                                pick_up_comment=more_info,
                                                user=request.user
                                                )

        return render(request, "form-confirmation.html")


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('landing_page'))

        else:
            return redirect(reverse('register'))


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            new_user = User.objects.create_user(email=email, password=password, first_name=name,
                                                last_name=surname)
        return redirect(reverse('login'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("landing_page"))


class UserProfileView(View):
    def get(self, request):
        user = request.user
        donations = Donations.objects.filter(user_id=user.id)
        return render(request, 'user_profile.html', {'user': user, "donations": donations})


class FilterInstitutionsInFormView(View):
    def get(self, request):
        categories_list = request.GET.getlist('categories')
        institutions_qs = Institution.objects.filter(categories__in=categories_list).distinct()
        institutions = [inst.id for inst in institutions_qs]
        return JsonResponse({'institutions': institutions})


class ArchiveDonationView(View):
    def post(self, request, donation_id, is_taken):
        donation = get_object_or_404(Donations, pk=donation_id)
        donation.is_taken = is_taken
        donation.save()

        return HttpResponse(status=204)


class UserUpdateView(View):

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, "user_update.html", {"form": form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('user_profile'))
