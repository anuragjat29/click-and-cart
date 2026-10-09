import paytmchecksum
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from unicodedata import category
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt
import requests

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import product,contact, orders, orderupdate, orderitems


client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

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


def prodmatch(query, item):
    if query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower() or query in item.product_desc.lower():
        return 1
    else: return 0

def search(request):
    query = request.GET.get('search')
    allproducts = []
    catprod = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prodcat = product.objects.filter(category=cat)
        prod = [item for item in prodcat if prodmatch(query.lower(),item)]
        n = len(prod)
        nslides = (n + 3) // 4
        if len(prod) != 0:
            allproducts.append([prod, range(1, nslides), nslides])

    # allproducts = [[products, range(1, len(products)), nslides],
    #             [products, range(1, len(products)), nslides]]
    params = {'allproducts': allproducts, "msg":""}
    if(len(allproducts) == 0 or len(query) < 4):
        params['msg'] = "Pls enter a valid query"
    return render(request, "shop/search.html", params)

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


def productview(request,myid):
    prod =product.objects.filter(id=myid)
    return render(request,'shop/productview.html',{'product':prod[0]})


def checkout(request):
    if(request.method == "POST"):
        name = request.POST.get("name","")
        gmail = request.POST.get("email","")
        address1 = request.POST.get("address1","")
        address2 = request.POST.get("address2","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        zipcode = request.POST.get("zipcode","")
        phone = request.POST.get("phone","")
        cart = request.POST.get("cart","")
        cart = json.loads(cart)
        status="Pending"
        order = orders(name=name, gmail=gmail, address1=address1, address2=address2,amount=0, city=city, state=state, zip_code=zipcode, phone=phone,status=status)
        order.save()

        # order_updates = orderupdate(order=order, order_desc="Pending")
        # order_updates.save()

        amount = 0
        for id in cart:
            p = product.objects.get(id=id)
            price = p.price
            product_name = p # foreign key
            qty = cart[id]
            amount += (price * qty)
            orderitem = orderitems(order=order, product=product_name, price=price, qty=qty)
            orderitem.save()

        order.amount = amount
        order.save()

        razorpay_order = client.order.create({
                "amount": amount * 100,   # Razorpay uses paise
                "currency": "INR",
                "receipt": str(order.orders_id)
        })
        print(razorpay_order)
        print(razorpay_order["id"])

        return render(
            request,
            "shop/checkout.html",
            {
                'thank': True,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "razorpay_order_id": razorpay_order["id"],
                "razorpay_amount": amount * 100,
                "order_id": order.orders_id,
                "name": name,
                "gmail": gmail,
                "phone": phone
            }
        )
    return render(request, 'shop/checkout.html')

def backup(request):
    return render(request, 'shop/backup.html')


@csrf_exempt
def handlerequest(request):

    if request.method == "POST":

        data = json.loads(request.body)

        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")
        order_id = data.get("order_id")

        try:

            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })

            # Payment is genuinely verified
            order = orders.objects.get(
                orders_id=order_id
            )

            order.status = "Paid"
            order.save()

            orderupdate.objects.create(
                order=order,
                order_desc="Placed"
            )

            return JsonResponse({
                "status": "success",
                "order_id": order.orders_id
            })

        except Exception as e:

            print("RAZORPAY VERIFICATION ERROR:", e)

            return JsonResponse({
                "status": "failed"
            })



