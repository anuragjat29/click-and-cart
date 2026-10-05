from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from unicodedata import category
import json

from .models import product ,contact, orders , orderitems, orderupdate
from math import ceil
# Create your views here.
def index(request):
    # products = product.objects.all()
    # n = len(products)
    # nslides = n//4 + ceil((n/4) + (n//4)

    allproducts=[]
    catprod=product.objects.values('category','id')
    cats ={item['category'] for item in catprod}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n = len(prod)
        nslides = (n + 3)//4
        allproducts.append([prod, range(1,nslides), nslides])


    # allproducts = [[products, range(1, len(products)), nslides],
    #             [products, range(1, len(products)), nslides]]

    params={'allproducts':allproducts}
    return render(request,"shop/index.html", params)

    # products=product.objects.all()
    # # para=product.objects.get(product_name='SAMSUNG Galaxy S25 Ultra 5G')
    # n=len(products)
    # nslides=n//4 + ceil(n/4-(n//4))
    # para={'product':'products','no_of_slides':'nslides','range':range(1,nslides)}
    # return render(request,'shop/index.html')


def about(request):
    return render(request,'shop/about.html')

def contacts(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        gmail=request.POST.get('gmail','')
        phone=request.POST.get('phone','')
        text=request.POST.get('text','')
        contacts=contact(name=name, gmail=gmail, phone=phone, text=text)
        contacts.save()
    return render(request, 'shop/contact.html')

def get_cart_products(request):

    ids = request.GET.get("ids","")
    ids = ids.split(",")

    products = product.objects.filter(id__in=ids)
    data = []
    for p in products:
        data.append({
            'id': p.id,
            'product_name': p.product_name,
            'price': p.price
        })
    return JsonResponse(data,safe=False)


    return render(request, 'shop/contact.html')

def track(request):
    if request.method == "POST":
        order_id = request.POST.get("orderid","")
        gmail = request.POST.get("gmail","")
        updates = []
        orderitemdetails = []
        if(order_id != "" and gmail != ""):
            order = orders.objects.filter(orders_id = order_id,
                                        gmail=gmail)
            if(order.exists()):
                orderupdates = orderupdate.objects.filter(order = order[0])
                orderitem = orderitems.objects.filter(order=order[0])

                for o in orderupdates:
                    updates.append({
                        "desc":o.order_desc,
                        "time":o.timestamp
                    })
                for o in orderitem:
                    orderitemdetails.append({
                        "name" : o.product,
                        "price" : o.price,
                        "qty" : o.qty,
                        "total":o.price * o.qty
                    })

        if(len(updates) == 0):
            updates.append({"desc":'Sorry, We are not able to fetch this order for this id and email. Make sure to type correct order Id and email'})
        return render(request, 'shop/track.html',{"orderupdates":updates, "orderitems":orderitemdetails})

    return render(request, 'shop/track.html')

def search(request):
    return render(request,'shop/search.html')

def productview(request,myid):
    prod =product.objects.filter(id=myid)
    return render(request,'shop/productview.html',{'product':prod[0]})

def checkout(request):
    if(request.method == "POST"):
        name = request.POST.get("name","")
        gmail = request.POST.get("email","")
        amount = request.POST.get("amount","")
        address1 = request.POST.get("address1","")
        address2 = request.POST.get("address2","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        zipcode = request.POST.get("zipcode","")
        phone = request.POST.get("phone","")
        cart = request.POST.get("cart","")
        cart = json.loads(cart)
        order = orders(name=name, gmail=gmail, address1=address1, address2=address2,amount=amount, city=city, state=state, zip_code=zipcode, phone=phone)
        order.save()

        order_updates = orderupdate(order=order, order_desc="Placed")
        order_updates.save()
        for id in cart:
            p = product.objects.get(id=id)
            price = p.price
            name = p # foreign key
            qty = cart[id]
            orderitem = orderitems(order=order, product=name, price=price, qty=qty)
            orderitem.save()
        return render(request, 'shop/checkout.html',{'thank':1, 'id':order.orders_id})
    return render(request, 'shop/checkout.html')

def backup(request):
    return render(request, 'shop/backup.html')



