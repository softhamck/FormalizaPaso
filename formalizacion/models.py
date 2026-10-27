from django.contrib.auth.models import User
from django.db import models


class Negocio(models.Model):

    ACTIVIDADES = [
        ('ALIMENTOS', 'Alimentos y bebidas'),
        ('COMERCIO', 'Comercio o venta de productos'),
        ('BELLEZA', 'Belleza y cuidado personal'),
        ('CONFECCION', 'Confección, moda o accesorios'),
        ('ARTESANIAS', 'Artesanías y productos hechos a mano'),
        ('TRANSPORTE', 'Transporte o domicilios'),
        ('TECNOLOGIA', 'Tecnología o servicios digitales'),
        ('SERVICIOS', 'Servicios técnicos o profesionales'),
        ('OTRA', 'Otra actividad'),
    ]

    ESTADOS_FORMALIZACION = [
        ('SIN_INICIAR', 'Sin iniciar'),
        ('EN_PROCESO', 'En proceso'),
        ('FORMALIZADO', 'Formalizado'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='negocios'
    )

    nombre = models.CharField(max_length=150)

    actividad_economica = models.CharField(
        max_length=20,
        choices=ACTIVIDADES
    )

    municipio = models.CharField(max_length=80)

    numero_trabajadores = models.PositiveIntegerField(default=1)

    estado_formalizacion = models.CharField(
        max_length=20,
        choices=ESTADOS_FORMALIZACION,
        default='SIN_INICIAR'
    )

    def __str__(self):
        return self.nombre


class Tramite(models.Model):

    nombre = models.CharField(
        max_length=180,
        unique=True
    )

    descripcion = models.TextField()

    requisitos = models.TextField(
        blank=True
    )

    entidad_responsable = models.CharField(
        max_length=120
    )

    enlace_oficial = models.URLField(
        max_length=500,
        blank=True
    )

    costo_estimado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.nombre


class RutaFormalizacion(models.Model):

    negocio = models.ForeignKey(
        Negocio,
        on_delete=models.CASCADE,
        related_name='rutas'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    porcentaje_avance = models.PositiveIntegerField(
        default=0
    )

    activa = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f'Ruta de {self.negocio.nombre}'


class PasoRuta(models.Model):

    ESTADOS_PASO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('COMPLETADO', 'Completado'),
    ]

    ruta = models.ForeignKey(
        RutaFormalizacion,
        on_delete=models.CASCADE,
        related_name='pasos'
    )

    tramite = models.ForeignKey(
        Tramite,
        on_delete=models.CASCADE,
        related_name='pasos'
    )

    orden = models.PositiveIntegerField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_PASO,
        default='PENDIENTE'
    )

    fecha_limite = models.DateField(
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['orden']

        constraints = [
            models.UniqueConstraint(
                fields=['ruta', 'orden'],
                name='orden_unico_por_ruta'
            ),
            models.UniqueConstraint(
                fields=['ruta', 'tramite'],
                name='tramite_unico_por_ruta'
            ),
        ]

    def __str__(self):
        return f'{self.orden}. {self.tramite.nombre}'