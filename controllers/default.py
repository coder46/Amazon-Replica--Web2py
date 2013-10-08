# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to web2py!")
    #return dict(message=T('Hello World'))
    redirect(URL('search'))
    return 


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def show():
	product=db.product(request.args(0,cast=int)) or redirect(URL('index'))
	db.reviews.pid.default=product.id
	form=SQLFORM(db.reviews)
	if form.process().accepted:
		response.flash='Your review has been posted'
	comments=db(db.reviews.pid==product.id).select()
	return dict(product=product,comments=comments,form=form)

@auth.requires_login()
def buy():
	product=db.product(request.args(0,cast=int)) or redirect(URL('index'))
	#redirect(URL('show',args=(product.id)))
	if(product.quant==0):
		response.flash='Product is out of stock'
	else:
		db.purchase.insert(pid=product.id,cid=int(auth.user_id))
		#a=int(product.quant)-1
		db(db.product.id==product.id).update(quant=db.product.quant-1)
		#redirect(URL('show',args=(product.id)))
		#redirect(URL('show'))
	redirect(URL('show',args=product.id))

@auth.requires_login()
def shopcart():
	#records=db((db.purchase.pid==db.product.id)).select(db.product.ALL)
	#purch=db(db.purchase.pid>=0).select(db.purchase.cid)
	records=db((db.purchase.cid==int(auth.user_id)) & (db.purchase.pid==db.product.id)).select(db.product.ALL)
	#purch=db(db.purchase.cid==request.args(0,cast=int)).select(db.purchase.ALL)
	return dict(records=records)
def crt():
	return dict(form=crud.create(db.product))
	
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def search():
	form=SQLFORM.factory(
			Field('name','string',label=""),
			Field('cat','list:string',requires=IS_IN_SET(["BY NAME","BY TAGS","BY BRAND"]),label="")
			)
	#form.vars.name="Search"
	#if form.accepts(request,session):
	records=db(db.product.id>0).select(db.product.ALL,orderby=db.product.id)
	if form.process(session=None, formname='test').accepted:
		redirect(URL(r=request,f="search_results",args=(form.vars.name,form.vars.cat)))
		#redirect(URL(r=request,f="search_results",args=['form.vars.name','form.vars.cat']))
	elif form.errors:
		response.flash="ERRORS!!!"
	
	return dict(form=form,records=records)

def search_results():
	name=str(request.args[0])
	name=name.upper()
	cat=str(request.args[1])
	records=[]
	query=""
	if(cat=='BY_TAGS'):
		#query="(db.tags.tag==name) & (db.tags.pid==db.product.id)"
		records=db((db.tags.tag==name) & (db.tags.pid==db.product.id)).select(db.product.ALL,orderby=db.product.id)
	elif (cat=='BY_NAME'):
		#query="(db.product.name==name)"
		#return dict(message="fkhsdkjfh")
		records=db(db.product.name==name).select(db.product.ALL,orderby=db.product.id)
	elif (cat=='BY_BRAND'):	
		#query="(db.product"
		records=db((db.brands.name==name) & (db.brands.id==db.product.brand)).select(db.product.ALL,orderby=db.product.id)
	#records=db((db.tags.tag==name) & (db.tags.pid==db.product.id)).select(db.product.ALL,orderby=db.product.id)
	#records=db(query).select(db.product.ALL,orderby=db.product.id)
	return dict(records=records)
	#return dict(showcase=SHOWCASE(records),title='Search Results')
"""
def details():
    
    #take arg or redirect
    id = request.args(0) or redirect(URL('index'))
    
    #query filtered
    query =db.product.id==int(id)
    rows=db(query).select()   
    
    #return object
    showcase = SHOWCASE(rows)
    
    # if has data creates other objects   
    if rows:
        
        #page Title   
        row = rows[0]                  
        title = "%(brand)s - %(quant)s" % \
            dict(brand=row.brand,\
                 quant=row.quant)
        
        #Form config            
        #db.client.id_car.default = id
        #db.client.id_car.readable = False
        #db.client.id_car.writable = False 
        
        #cretes the form       
        #form = SQLFORM(db.client,formstyle='divs',submit_button='Send')
        
        #validation of the form   
        #if form.accepts(request, session):
            
        #    try:
        #        subject='Client %s wants to buy %s ' % (form.vars.name,form.vars.id_car)
        #        email_user(sender=form.vars.email,\
        #                   message='Tel: %s - Finance? %s - Change? %s - Date: %s '\
        #                            % (form.vars.tel,form.vars.finance,form.vars.change,form.vars.date),\
        #                   subject=subject)
        #    except Exception, e:
        #        pass               
                  
        #    response.flash = 'Accepted'
            
            #Success Message
        #    form = DIV(H3('Message sent, we will contact you soon'))
                
        #elif form.errors:
        #    response.flash = 'Errors'
                                        
        return dict(showcase=showcase,title=title,form=form)
        
    else:
        return dict(showcase=H1('car not found'))                 
    

"""

@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
