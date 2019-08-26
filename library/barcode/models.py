from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django_mysql import models as sqlModel
from datetime import datetime
from time import strftime
import re


class TinyIntegerField(models.SmallIntegerField):
    """
        Customized Class for creating a SmallIntegerField that is represented on the database as a Tinyint field 
        of MySQL rather than the usual SmallInteger field of Django.
    """
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class UnixTimestampField(models.DateTimeField):
    """
        Customized Class for creating a DateTimeField that is represented on the database as a TIMESTAMP field 
        of MySQL rather than the usual DATETIME field of Django.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ=['TIMESTAMP']
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())


class Biblio(models.Model): 
    """
        A class representing a Django Model of Koha Database table **biblio**
    """

    biblionumber = models.AutoField(primary_key=True)
    frameworkcode = models.CharField(max_length=4)
    author = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    title = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    unititle = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    notes = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    serial = TinyIntegerField(blank=True, null=True, default=None)
    seriestitle = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    copyrightdate = models.SmallIntegerField(blank=True, null=True, default=None)
    timestamp = UnixTimestampField(auto_created=True)
    datecreated = models.DateField(default=None)
    abstract = sqlModel.SizedTextField(3, blank=True, null=True, default=None)

    def get_author(self):
        regex = re.compile("[^a-zA-Z.'-,\s]")
        if self.author:
            return regex.sub('', self.author)
        else:
            return ''

    class Meta:
        """
        .. warning:: This class is very important. **Do not modify it unless you are very sure of it.**

            managed - *Tells Django not to manage this table by yourself. It is managed by 3rd party.*
            db_table - *Forces Django to use this table name rather than its own naming convention.*
            app_label - *This label is used for Database Routers*

        """
        managed = False
        db_table = 'biblio'
        app_label = 'koha_data'


class BiblioMetadata(models.Model):
    """
        A class representing a Django Model of Koha Database table **biblio_metadata**
    """

    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber')
    format = models.CharField(max_length=16)
    marcflavour = models.CharField(max_length=16)
    metadata = sqlModel.SizedTextField(4)

    class Meta:
        """
        .. warning:: This class is very important. **Do not modify it unless you are very sure of it.**

            managed - *Tells Django not to manage this table by yourself. It is managed by 3rd party.*
            db_table - *Forces Django to use this table name rather than its own naming convention.*
            app_label - *This label is used for Database Routers*

        """
        managed = False
        db_table = 'biblio_metadata'
        unique_together = (('biblionumber', 'format', 'marcflavour'),)
        app_label = 'koha_data'

class Biblioitems(models.Model):
    """
        A class representing a Django Model of Koha Database table **biblioitems**
    """

    biblioitemnumber = models.AutoField(primary_key=True, default=None)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber', default=0)
    volume = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    number = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    itemtype = models.CharField(max_length=10, blank=True, null=True, default=None)
    isbn = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    issn = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    ean = models.CharField(max_length=13, blank=True, null=True, default=None)
    publicationyear = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    publishercode = models.CharField(max_length=255, blank=True, null=True, default=None)
    volumedate = models.DateField(blank=True, null=True, default=None)
    volumedesc = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    collectiontitle = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    collectionissn = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    collectionvolume = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    editionstatement = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    editionresponsibility = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    timestamp = UnixTimestampField(auto_created=True)
    illus = models.CharField(max_length=255, blank=True, null=True, default=None)
    pages = models.CharField(max_length=255, blank=True, null=True, default=None)
    notes = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    size = models.CharField(max_length=255, blank=True, null=True, default=None)
    place = models.CharField(max_length=255, blank=True, null=True, default=None)
    lccn = models.CharField(max_length=25, blank=True, null=True, default=None)
    url = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    cn_source = models.CharField(max_length=10, blank=True, null=True, default=None)
    cn_class = models.CharField(max_length=30, blank=True, null=True, default=None)
    cn_item = models.CharField(max_length=10, blank=True, null=True, default=None)
    cn_suffix = models.CharField(max_length=10, blank=True, null=True, default=None)
    cn_sort = models.CharField(max_length=255, blank=True, null=True, default=None)
    agerestriction = models.CharField(max_length=255, blank=True, null=True, default=None)
    totalissues = models.IntegerField(blank=True, null=True, default=None, validators=[MaxValueValidator(9999999999)])

    class Meta:
        """
            This class is very important. **Do not modify it unless you are very sure of it.**

            managed - *Tells Django not to manage this table by yourself. It is managed by 3rd party.*
            db_table - *Forces Django to use this table name rather than its own naming convention.*
            app_label - *This label is used for Database Routers*

        """
        managed = False
        db_table = 'biblioitems'
        app_label = 'koha_data'

class Branches(models.Model):
    """
        A class representing a Django Model of Koha Database table **branches**
    """
    branchcode = models.CharField(primary_key=True, max_length=10)
    branchname = sqlModel.SizedTextField(3, default=None)
    branchaddress1 = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchaddress2 = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchaddress3 = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchzip = models.CharField(max_length=25, blank=True, null=True, default=None)
    branchcity = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchstate = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchcountry = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    branchphone = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchfax = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchemail = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchreplyto = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchreturnpath = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    branchurl = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    issuing = TinyIntegerField(blank=True, null=True, default=None)
    branchip = models.CharField(max_length=15, blank=True, null=True, default=None)
    branchprinter = models.CharField(max_length=100, blank=True, null=True, default=None)
    branchnotes = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    opac_info = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    geolocation = models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        """
            This class is very important. **Do not modify it unless you are very sure of it.**

            managed - *Tells Django not to manage this table by yourself. It is managed by 3rd party.*
            db_table - *Forces Django to use this table name rather than its own naming convention.*
            app_label - *This label is used for Database Routers*

        """
        managed = False
        db_table = 'branches'
        app_label = 'koha_data'

class Items(models.Model):
    """
        A class representing a Django Model of Koha Database table **items**
    """
    itemnumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, models.DO_NOTHING, db_column='biblionumber', default=0)
    biblioitemnumber = models.ForeignKey(Biblioitems, models.DO_NOTHING, db_column='biblioitemnumber', default=0)
    barcode = models.CharField(unique=True, max_length=20, blank=True, null=True, default=None)
    dateaccessioned = models.DateField(blank=True, null=True, default=None)
    booksellerid = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    homebranch = models.ForeignKey(Branches, models.DO_NOTHING, db_column='homebranch', blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None)
    replacementprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=None)
    replacementpricedate = models.DateField(blank=True, null=True, default=None)
    datelastborrowed = models.DateField(blank=True, null=True, default=None)
    datelastseen = models.DateField(blank=True, null=True, default=None)
    stack = TinyIntegerField(blank=True, null=True, default=None)
    notforloan = models.IntegerField(default=0)
    damaged = models.IntegerField(default=0)
    itemlost = models.IntegerField(default=0)
    itemlost_on = models.DateTimeField(blank=True, null=True, default=None)
    withdrawn = models.IntegerField(default=0)
    withdrawn_on = models.DateTimeField(blank=True, null=True, default=None)
    itemcallnumber = models.CharField(max_length=255, blank=True, null=True, default=None)
    coded_location_qualifier = models.CharField(max_length=10, blank=True, null=True, default=None)
    issues = models.SmallIntegerField(blank=True, null=True, default=None)
    renewals = models.SmallIntegerField(blank=True, null=True, default=None)
    reserves = models.SmallIntegerField(blank=True, null=True, default=None)
    restricted = TinyIntegerField(blank=True, null=True, default=None)
    itemnotes = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    itemnotes_nonpublic = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    holdingbranch = models.ForeignKey(Branches, models.DO_NOTHING, db_column='holdingbranch', blank=True, null=True, default=None)
    paidfor = sqlModel.SizedTextField(3, blank=True, null=True, default=None)
    timestamp = UnixTimestampField(auto_created=True)
    location = models.CharField(max_length=80, blank=True, null=True, default=None)
    permanent_location = models.CharField(max_length=80, blank=True, null=True, default=None)
    onloan = models.DateField(blank=True, null=True, default=None)
    cn_source = models.CharField(max_length=10, blank=True, null=True, default=None)
    cn_sort = models.CharField(max_length=255, blank=True, null=True, default=None)
    ccode = models.CharField(max_length=10, blank=True, null=True, default=None)
    materials = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    uri = models.CharField(max_length=255, blank=True, null=True, default=None)
    itype = models.CharField(max_length=10, blank=True, null=True, default=None)
    more_subfields_xml = sqlModel.SizedTextField(4, blank=True, null=True, default=None)
    enumchron = sqlModel.SizedTextField(2, blank=True, null=True, default=None)
    copynumber = models.CharField(max_length=32, blank=True, null=True, default=None)
    stocknumber = models.CharField(max_length=32, blank=True, null=True, default=None)
    new_status = models.CharField(max_length=32, blank=True, null=True, default=None)
    shelf = models.CharField(max_length=45, blank=True, null=True, default=None)
    bill_no = models.CharField(max_length=100, blank=True, null=True, default=None)
    inv = models.CharField(max_length=100, blank=True, null=True, default=None)
    inv_det = models.CharField(max_length=100, blank=True, null=True, default=None)
    vendor = models.CharField(max_length=200, blank=True, null=True, default=None)
    discount = models.CharField(max_length=45, blank=True, null=True, default=None)
    conv_rate = models.CharField(max_length=45, blank=True, null=True, default=None)
    currency = models.CharField(max_length=45, blank=True, null=True, default=None)

    def get_item_callnumber(self):
        """
            This definition splits the itemcallnumber, if exists, and returns the entire substring from the
            start till the first match of the Alphabetic character.
        """

        if self.itemcallnumber:
            '''
                \W - non-alphabetic characters
                \d - non-numeric characters
                [^\W\d] - not of (non-alphabetic or non-numeric characters)
            '''

            callList = self.itemcallnumber.split()
            if len(callList) == 1:
                match = re.compile("[^\W\d]+").search(self.itemcallnumber[::-1])
                if match:
                    matchLen = match.end() - match.start()
                    if matchLen <= 3:
                        return self.itemcallnumber[:-match.end()]
                    else:
                        return self.itemcallnumber[:-(match.end()-(matchLen-3))]
                else:
                    return callList[0]
            else:
                callNum = ""
                for i in range(len(callList)-1):
                    callNum += callList[i] + " "

                match = re.search('[a-zA-Z]', callList[-1])
                if not (match and match.start() == 0) :
                    callNum += callList[-1] + " "

                return callNum.rstrip()


        return ''

    def get_author_mark(self):
        """
            This definition splits the itemcallnumber, if exists, and returns the entire substring from the
            first match of the Alphabetic character till the end.
        """

        if self.itemcallnumber:
            '''
                \W - non-alphabetic characters
                \d - non-numeric characters
                [^\W\d] - not of (non-alphabetic or non-numeric characters)
            '''
            callList = self.itemcallnumber.split()
            if len(callList) == 1:
                match = re.compile("[^\W\d]+").search(self.itemcallnumber[::-1])
                if match:
                    matchLen = match.end() - match.start()
                    if matchLen <= 3:
                        return self.itemcallnumber[-match.end():]
                    else:
                        return self.itemcallnumber[-(match.end()-(matchLen-3)):]
                else:
                    return ''
            else:
                match = re.search('[a-zA-Z]', callList[-1])
                if match and match.start() == 0 :
                    return callList[-1]

        return ''

    class Meta:
        """
            This class is very important. **Do not modify it unless you are very sure of it.**

            managed - *Tells Django not to manage this table by yourself. It is managed by 3rd party.*
            db_table - *Forces Django to use this table name rather than its own naming convention.*
            app_label - *This label is used for Database Routers*

        """
        managed = False
        db_table = 'items'
        app_label = 'koha_data'
