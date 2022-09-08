from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from django.views.generic import DetailView
from rest_framework.response import Response

from .models import BankOffer
from .serializers import BankOfferSerializer
from .forms import ClientRequest


class BankOfferViewSet(viewsets.ModelViewSet):
    queryset = BankOffer.objects.all()
    serializer_class = BankOfferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price_min', 'price_max',
                        'term_min', 'term_max']

    # ?price=700000&deposit=100000&term=10
    def get_queryset(self):
        price = self.request.query_params.get('price')
        deposit = self.request.query_params.get('deposit')
        term = self.request.query_params.get('term')
        if price and deposit and term:
            self.queryset = BankOffer.objects.filter(price_min__lte=price,
                                                     price_max__gte=price,
                                                     term_min__lte=term,
                                                     term_max__gte=term)
        return self.queryset


class BankOfferDetail(DetailView):
    model = BankOffer
    template_name = 'MorOC/offer_datails.html'
    context_object_name = 'offer'


def index(request):
    form = ClientRequest()
    bank_offers = BankOffer.objects.all()
    error = ''
    payments = []

    if request.method == 'POST':
        form = ClientRequest(request.POST)
        if form.is_valid():
            bank_offers = filter_bank_offers(form)
            for bank_offer in bank_offers:
                try:
                    payment = calc_payments(bank_offer, form)
                    payments.append(payment)
                except Exception as exc:
                    error = exc.args[0]

            return render(request, 'MorOC/index.html', {"bank_offers": bank_offers,
                                                        "form": form,
                                                        "payments": payments,
                                                        "error": error})

    return render(request, 'MorOC/index.html', {"bank_offers": bank_offers,
                                                "form": form,
                                                })


def calc_payments(bank_offer, form):
    payment = None
    mr = bank_offer.max_mortgage_rate / (12 * 100)
    price = int(form.data['price'])
    start_sum = int(form.data['start_sum'])
    for_year = int(form.data['for_year'])
    if for_year > 0:
        payment = (price - start_sum) * mr / (1 - (1 + mr) ** (-12 * for_year))
    else:
        raise Exception('Срок не должен быть нулевым или отрицательным!')
    return int(payment)


def filter_bank_offers(form):
    bank_offers = BankOffer.objects.filter(price_min__lte=form.data['price'],
                                          price_max__gte=form.data['price'],
                                          term_min__lte=form.data['for_year'],
                                          term_max__gte=form.data['for_year'])
    print(bank_offers)
    return bank_offers
