from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.http import JsonResponse
from .models import Books
from django.core.paginator import Paginator
def home(request):

    try:
        Books_obj=Books.objects.all()
        pagination = Paginator(Books_obj,24)
        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        return render(request, 'home.html', {'page_obj': page_obj})
    except Exception as e:
        return JsonResponse({'error': e}, status=400)


def search_view(request):

    search_query = request.GET.get('query', '')
    
    if search_query:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Origin': 'https://www.worldofbooks.com',
            'Referer': 'https://www.worldofbooks.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = '{"requests":[{"indexName":"shopify_products_apac","params":"clickAnalytics=true&facets=%5B%22author%22%2C%22availableConditions%22%2C%22bindingType%22%2C%22console%22%2C%22hierarchicalCategories.lvl0%22%2C%22platform%22%2C%22priceRanges%22%2C%22productType%22%2C%22publisher%22%5D&filters=fromPrice%20%3E%200%20AND%20inStock%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&maxValuesPerFacet=10&page=0&query='+str(
            search_query)+'&tagFilters=&userToken=anonymous-8cb3fd89-e94b-437a-87f7-7c331d574639"}]}'

        response = requests.post(
            'https://ar33g9njgj-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.22.0)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.62.0)%3B%20JS%20Helper%20(3.16.0)&x-algolia-api-key=365f3003b2ac7d8bea79190084879565&x-algolia-application-id=AR33G9NJGJ',
            headers=headers,
            data=data,
        )

        if response.status_code == 200:
            if response.json().get('results'):

                products = []

                data = response.json()
                hits = data.get('results')[0].get('hits')
                for hit in hits:
                    if not Books.objects.filter(isbn=hit.get('isbn13')).exists():
                        book = Books(
                            title=hit.get('shortTitle'),
                            isbn=hit.get('isbn13'),
                            imageURL=hit.get('imageURL'),
                            author=hit.get('author'),
                            url='https://www.worldofbooks.com/en-au/products/' +
                                hit.get('productHandle')
                        )
                        products.append(book)
                if products:
                    Books.objects.bulk_create(products)

                response_data = [{
                    'title': hit.get('shortTitle'),
                    'isbn': hit.get('isbn13'),
                    'imageURL': hit.get('imageURL'),
                    'author': hit.get('author'),
                    'url': 'https://www.worldofbooks.com/en-au/products/' +
                    hit.get('productHandle')
                } for hit in hits]
                return JsonResponse(response_data, safe=False)
            else:
                return JsonResponse({'error': 'No results found'}, status=404)
        else:
            return JsonResponse({'error': 'Failed to fetch data', 'status_code': response.status_code}, status=response.status_code)
    else:
        return JsonResponse({'error': 'Search query is empty'}, status=400)