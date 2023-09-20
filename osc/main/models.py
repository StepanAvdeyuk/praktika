from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


SIGNAL_SOURCES = (
    ('SOUR1', 'Source 1'),
    ('SOUR2', 'Source 2')
)

CHANNEL_SOURCES = (
    ('CH1', 'Channel 1'),
    ('CH2', 'Channel 2'),
    # ('CH3', 'Channel 3'),
)

SIGNAL_FORMS = (
    ('SIN', 'Гармонический'),
    ('SQU', 'Меандр'),
    ('RAMP', 'Треугольный')
)

SHOW_GRAPH = (
    ('TRUE', 'Да'),
    ('FALSE', 'Нет'),
)


class Power(models.Model):
    power_channel = models.CharField(max_length=50, choices=CHANNEL_SOURCES)
    voltage = models.FloatField(
        default=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(30)
        ]
    )



class SignalGenerator(models.Model):
    channel = models.CharField(max_length=50, choices=SIGNAL_SOURCES)
    sig_form = models.CharField(max_length=50, choices=SIGNAL_FORMS)
    frequency = models.FloatField(
        default=10000,
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(100000)
        ]
    )
    amplitude = models.FloatField(
        default=5,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(18)
        ]
    )


class Oscilloscope(models.Model):
    show_graph = models.CharField(max_length=50, choices=SHOW_GRAPH, default=SHOW_GRAPH[0][0])
    ch_scale = models.FloatField(
        default=0.2,
        validators=[
            MinValueValidator(0.0001),
            MaxValueValidator(1)
        ]
    )
    time_base = models.FloatField(
        default=0.0002,
        validators=[
            MinValueValidator(0.000001),
            MaxValueValidator(0.1)
        ]
    )
    offset_x = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )
    offset_y = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )

    show_graph2 = models.CharField(max_length=50, choices=SHOW_GRAPH, default=SHOW_GRAPH[0][0])
    ch_scale2 = models.FloatField(
        default=0.2,
        validators=[
            MinValueValidator(0.0001),
            MaxValueValidator(1)
        ]
    )
    time_base2 = models.FloatField(
        default=0.0002,
        validators=[
            MinValueValidator(0.000001),
            MaxValueValidator(0.1)
        ]
    )
    offset_x2 = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )
    offset_y2 = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )

    show_graph3 = models.CharField(max_length=50, choices=SHOW_GRAPH, default=SHOW_GRAPH[0][0])
    ch_scale3 = models.FloatField(
        default=0.2,
        validators=[
            MinValueValidator(0.0001),
            MaxValueValidator(1)
        ]
    )
    time_base3 = models.FloatField(
        default=0.0002,
        validators=[
            MinValueValidator(0.000001),
            MaxValueValidator(0.1)
        ]
    )
    offset_x3 = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )
    offset_y3 = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )

    show_graph4 = models.CharField(max_length=50, choices=SHOW_GRAPH, default=SHOW_GRAPH[0][0])
    ch_scale4 = models.FloatField(
        default=0.2,
        validators=[
            MinValueValidator(0.0001),
            MaxValueValidator(1)
        ]
    )
    time_base4 = models.FloatField(
        default=0.0002,
        validators=[
            MinValueValidator(0.000001),
            MaxValueValidator(0.1)
        ]
    )
    offset_x4 = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )
    offset_y4 = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1),
            MaxValueValidator(1)
        ]
    )

    def __str__(self):
        return self.channel
