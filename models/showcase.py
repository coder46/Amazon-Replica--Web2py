# coding: utf8
def SHOWCASE(rows):
    """Creates a car showcase"""
    
    #Armazena a estrutura do HTML que será interpolado    
    placeholder = """
    <div class='vcar' style='width:500px;border:1px solid gray;'>
        <div class='vcpict' style='float:left;margin:10px;'>
            <a href='%(url)s'>        
                <img border='0' width='100px' height='100px'
                    src='%(urlpic)s'>
            </a>
        </div>
        <div class='vcdata' style='padding:10px;margin:10px;'>
            <span class='vcdtitle'>
                <strong>
                %(brand)s - %(quant)s
                </strong>
            </span>
            <div style='padding: 10px 100px 1px;'>
            <ul class='vcdinfo'>
                <li>%(brand)s</li>
                <li>%(quant)s</li>
            <ul>
            </div>
            <p class='vcdtext'>
                <blockquote>
                %(descr)s
                </blockquote>
            </p>
            <span class='vcdprice' 
                  style="float:right;color:blue;font-size:20px;">
                <strong>%(price)s</strong>
            </span>                    
        </div>
    </div>
    """
    
    #Caso existam registros em "rows" efetua a interpolação
    if rows:
        showcase = [placeholder % dict(url=URL('details', args=row.id),\
                                    urlpict=URL('download',args=row.pict),\
                                    brand=rows.brand.name,\
                                    quant=row.quant,\
                                    desc=row.desc,\
                                    price=Money(row.price),\
                                    ) for row in rows ]
                                
    else:
        showcase = ["<h1 class='nothing'>No cars were found</h1>"]
    
    return showcase
