import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect

from backend.business_logic import FiestaService, InvitadoService, ValidationError

fiesta_service = FiestaService()
invitado_service = InvitadoService()


# ─── JSON API endpoints ──────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def fiestas(request):
    if request.method == 'GET':
        data = fiesta_service.listar_fiestas()
        return JsonResponse({'fiestas': data, 'count': len(data)})

    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            result = fiesta_service.crear_fiesta(payload)
            return JsonResponse(result, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'error': str(exc)}, status=exc.status_code)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def invitados(request):
    if request.method == 'GET':
        fiesta_id = request.GET.get('fiesta_id')
        data = invitado_service.listar_invitados(int(fiesta_id) if fiesta_id else None)
        return JsonResponse({'invitados': data, 'count': len(data)})

    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            result = invitado_service.aceptar_invitado(payload)
            return JsonResponse(result, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'error': str(exc)}, status=exc.status_code)


@csrf_exempt
@require_http_methods(['PATCH'])
def invitado_estado(request, invitado_id):
    try:
        payload = json.loads(request.body)
        estado = payload.get('estado', '')
        result = invitado_service.actualizar_estado(invitado_id, estado)
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except ValidationError as exc:
        return JsonResponse({'error': str(exc)}, status=exc.status_code)


# ─── Server-side rendered views — Frontend Invitados ────────────────────────

def invitados_home(request):
    fiestas = fiesta_service.listar_fiestas()
    context = {'fiestas': fiestas, 'active': 'invitados'}
    return render(request, 'invitados/home.html', context)


def invitados_fiesta(request, fiesta_id):
    try:
        fiesta = fiesta_service.obtener_fiesta(fiesta_id)
    except ValidationError:
        return redirect('invitados_home')

    invitados = invitado_service.listar_invitados(fiesta_id)
    mensaje = None
    error = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        contacto = request.POST.get('contacto', '').strip()
        try:
            invitado_service.aceptar_invitado({
                'fiesta_id': fiesta_id,
                'nombre': nombre,
                'contacto': contacto,
            })
            mensaje = f'¡{nombre} fue registrado exitosamente!'
            invitados = invitado_service.listar_invitados(fiesta_id)
            fiesta = fiesta_service.obtener_fiesta(fiesta_id)
        except ValidationError as exc:
            error = str(exc)

    context = {
        'fiesta': fiesta,
        'invitados': invitados,
        'mensaje': mensaje,
        'error': error,
        'active': 'invitados',
    }
    return render(request, 'invitados/fiesta_detail.html', context)


# ─── Server-side rendered views — Frontend Localización ─────────────────────

def localizacion_home(request):
    fiestas = fiesta_service.listar_fiestas()
    context = {'fiestas': fiestas, 'active': 'localizacion'}
    return render(request, 'localizacion/home.html', context)


def localizacion_nueva(request):
    mensaje = None
    error = None

    if request.method == 'POST':
        try:
            lat_raw = request.POST.get('latitud', '').strip()
            lng_raw = request.POST.get('longitud', '').strip()
            cap_raw = request.POST.get('capacidad', '0').strip()

            payload = {
                'nombre': request.POST.get('nombre', '').strip(),
                'ubicacion': request.POST.get('ubicacion', '').strip(),
                'latitud': float(lat_raw) if lat_raw else None,
                'longitud': float(lng_raw) if lng_raw else None,
                'capacidad': int(cap_raw),
                'fecha': request.POST.get('fecha', ''),
                'hora': request.POST.get('hora', ''),
                'descripcion': request.POST.get('descripcion', '').strip(),
            }
            fiesta_service.crear_fiesta(payload)
            mensaje = '¡Fiesta registrada exitosamente!'
        except ValidationError as exc:
            error = str(exc)
        except (ValueError, TypeError):
            error = 'Capacidad, latitud y longitud deben ser valores numéricos válidos.'

    context = {'mensaje': mensaje, 'error': error, 'active': 'localizacion'}
    return render(request, 'localizacion/nueva.html', context)
