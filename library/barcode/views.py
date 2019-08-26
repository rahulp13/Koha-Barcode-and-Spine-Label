from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render, HttpResponse
from django.db.models.functions import Cast
from django.db.models import IntegerField
import xml.etree.ElementTree as ET
from django.conf import settings
from .models import Items, BiblioMetadata
import base64, os, re

# Create your views here.
@login_required
def index(request):
    """
        This definition handles the POST request from the HTML Form. If the form parameters are correct, 
        then a query is made to the **Koha Database** based on whether it is a single query or a range of 
        queries. The retrieved data is wrapped in a dictionary "context" and request is rendered back. 
        It requires the user to be logged in.

        :param request: *A POST request from the HTML Form*

        :return: `render() <https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/#django.shortcuts.render>`_ - *A function with request, redirection to the only template and context data*

    """

    # A dictionary that will be passed to template from the server
    context = dict()

    #Check whether a form is POSTed or not
    if request.method == "POST":

        """ ---------------------------------------------------------------------------------------------
        #Get the value of the selected option
        typeReq = request.POST.get('type')

        #If no other option than the default one is not selected, then proceed
        if typeReq != '1':
            data = None

            #Check if the request was for a single barcode
            if request.POST['barcode_num']:
                #Get data from the Koha database where barcode value matches the requested value.
                data = Items.objects.filter(barcode=request.POST['barcode_num'])

            #Else, check if the request was for a range of barcodes
            elif request.POST['barcode_start'] and request.POST['barcode_end']:
                #Get data from the Koha database where the barcode value lies within the requested range of values.
                #The barcode values from the Koha table are first converted into integer fields and then data is retrieved.
                data = Items.objects.annotate(barcode_int=Cast('barcode', IntegerField())).filter(barcode_int__range=(request.POST['barcode_start'], request.POST['barcode_end']))

            if data and len(data) != 0:
                #Check if request is for Barcode Printing
                if (typeReq == '2'):
                    #set the context with the Koha data
                    context['data'] = data
                    #set a flag for template processing
                    context['bar'] = 'bar'

                #Else, check if request is for Spine Label Printing
                elif (typeReq == '3'):
                    #set the context with the Koha data
                    context['data'] = data
                    #set a flag for template processing
                    context['spine'] = 'spine'

        -----------------------------------------------------------------------------------------------"""

        data = None

        #Check if the request was for a single barcode
        if request.POST['barcode_num']:
            #Get data from the Koha database where barcode value matches the requested value.
            data = Items.objects.filter(barcode=request.POST['barcode_num']).filter(withdrawn=0)

        #Else, check if the request was for a range of barcodes
        elif request.POST['barcode_start'] and request.POST['barcode_end']:
            start = request.POST['barcode_start']
            end = request.POST['barcode_end']

            if start.isdecimal() and end.isdecimal():
                #Get data from the Koha database where the barcode value lies within the requested range of values.
                #The barcode values from the Koha table are first converted into integer fields and then data is retrieved.
                data = Items.objects.annotate(barcode_int=Cast('barcode', IntegerField())).filter(barcode_int__range=(request.POST['barcode_start'], request.POST['barcode_end'])).filter(withdrawn=0)

            else:
                match_from = re.compile("[^\W\d]+").search(start)
                match_to = match = re.compile("[^\W\d]+").search(end)

                if start[match_from.start():match_from.end()] == end[match_to.start():match_to.end()]:
                    start_index = int(start[match_from.end():])
                    end_index = int(end[match_to.end():])
                    startCharCode = start[match_from.start():match_from.end()]

                    data = Items.objects.filter(barcode=startCharCode + str(start_index)).filter(withdrawn=0)

                    for i in range(start_index+1, end_index+1):
                        data = data | Items.objects.filter(barcode=startCharCode+str(i)).filter(withdrawn=0)
                        

        if data and len(data) != 0:
            data = list(data)

            for val in data:
                if not val.biblionumber.author:
                    result = BiblioMetadata.objects.filter(biblionumber=val.biblionumber.biblionumber)
                    root = ET.fromstring(result[0].metadata)
                    for field in root.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                        sub = field.find("{http://www.loc.gov/MARC21/slim}subfield")
                        if field.attrib['tag'] == '700':
                            if sub.attrib['code'] == "a":
                                val.biblionumber.author = sub.text
                                if sub.text:
                                    break



            context['data'] = data

        """--------------------------------------------------------------------------------------------"""

        # SELECT    ExtractValue((     SELECT metadata     FROM biblio_metadata     WHERE       biblionumber=420),       '//datafield[@tag="700"]/subfield[@code>="a"]') AS ITEM;



    return render(request, 'barcode/index.html', context)



@login_required
def encodeFont(request):
    if request.method == "POST":
        fileName = request.POST.get('text')
        file = open(os.path.join(settings.STATICFILES_DIRS[0], fileName), 'rb')
        file_content = file.read()
        encode = base64.b64encode(file_content).decode('ascii')
        return HttpResponse(repr(encode))