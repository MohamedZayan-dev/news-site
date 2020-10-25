from django.shortcuts import render, redirect, HttpResponse
import requests
import json

def getData(page):
    response = requests.get('https://content.guardianapis.com/search?show-fields=thumbnail&page-size=30&q='+page+'&api-key=test')
    jsonResponse = response.json()
    singleElement = {}
    data = []
    context = {}
    results = jsonResponse['response']['results']
    if len(results) != 0:
        for result in results :
            title = result['webTitle']
            # default thumbnail (will be used if result has no 'field' element)
            thumbnail = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSUu8ud8EJ-CyKpl8lRt-rMb6owI8rZghqsmQ&usqp=CAU'
            if 'fields' in result:
                thumbnail = result['fields']['thumbnail']
            sectionName = result['sectionName']
            id = result['id']
            singleElement['title'] = title
            singleElement['thumbnail'] = thumbnail
            singleElement['sectionName'] = sectionName
            singleElement['id'] = id
            data.append(singleElement.copy())
            context = {'data':data, 'page':page}
    return context

#all pages other than default(home)
def subPages(request, page):
    if request.method == 'POST':
        context = getData(request.POST.get('search'))
    else:
        context = getData(page)

    return render(request, 'view/base_pages.html',context)
    
#reason for home having its own view is that so it can be the default url for the site
def home(request):
    if request.method == 'POST':
        context = getData(request.POST.get('search'))
    else:
        context = getData('')

    return render(request, 'view/base_pages.html',context)

def details(request, id):
    url = 'https://content.guardianapis.com/'+id+'?show-fields=thumbnail%2CbodyText&api-key=test'
    response = requests.get(url)
    jsonResponse = response.json()
    element = jsonResponse['response']['content']
    # default thumbnail (will be used if element has no thumbnail)
    thumbnail = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSUu8ud8EJ-CyKpl8lRt-rMb6owI8rZghqsmQ&usqp=CAU'
    bodyText = ''
    if 'fields' in element:
        if 'thumbnail' in element['fields']:
            thumbnail = element['fields']['thumbnail']
        if 'bodyText' in element['fields']:
            bodyText = element['fields']['bodyText']
    context = {'webTitle': element['webTitle'], 'webPublicationDate': element['webPublicationDate']
                ,'thumbnail': thumbnail, 'bodyText': bodyText}
    return render(request, 'view/details.html', context)


