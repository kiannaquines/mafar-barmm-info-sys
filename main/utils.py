from django.contrib import messages


def request_message(request, message, tag):
    if tag == 'success':
        messages.success(request=request, message=message, extra_tags=tag)
    elif tag == 'danger':
        messages.error(request=request, message=message, extra_tags=tag)
    elif tag == 'warning':
        messages.warning(request=request, message=message, extra_tags=tag)
    else:
        messages.info(request=request, message=message, extra_tags=tag)