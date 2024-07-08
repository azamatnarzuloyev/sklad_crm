from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template 
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
 
    template = get_template(template_src)
    html  = template.render(context_dict)
    
    # encod = html.encode("utf-16")
    # data = encod.decode("utf-16")
 
    

    result = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



# ISO-8859-1