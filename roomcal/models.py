from django.db import models
import datetime

# teach South about my new field
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^roomcal\.models\.PriceField"])

# Create your models here.

class PriceField(models.DecimalField):
    def __init__(self,*args,**kwargs):
        kwargs["decimal_places"] = 2
        kwargs["max_digits"] = 6
        models.DecimalField.__init__(self, *args, **kwargs)

class Room(models.Model):
    name = models.CharField(max_length=500)
    status = models.CharField(max_length=30, choices=(('live','Live on site'),('hidden','Hidden from public')))
    description = models.TextField()
    min_persons = models.IntegerField()
    max_persons = models.IntegerField()

class SlotManager(models.Manager):
    def create_slots_in_range(self, room, base_price, extra_person_price,
                              start_date, end_date, slot_times, duration_mins, buffer_mins):
        for day_date in (start_date + datetime.timedelta(days) for days in range(0, (end_date - start_date).days)):
            for slot_time in slot_times:
                #self.get( start_time__gte
                s = Slot(
                    room = room,
                    base_price = base_price,
                    extra_person_price = extra_person_price,
                    start = datetime.datetime.combine(day_date, slot_time),
                    end = datetime.datetime.combine(day_date, slot_time) + datetime.timedelta(0, 60 * duration_mins, 0)
                )
                s.save()
    def get_calendar(self, start):
        slots = Slot.objects.filter(start__gte = start, start__lte = start + datetime.timedelta(90))
        days = []
        # work back to beginning of month for a nice tidy calendar
        tidy_start = datetime.datetime(start.year, start.month, 1, 0, 0)
        extra_days = (start - tidy_start).days
        for day in (tidy_start + datetime.timedelta(n) for n in range(0, 90 + extra_days)):
            # clamp to midnight
            day.replace(day.year, day.month, day.day, 0, 0, 0, 0)
            days.append( {
                "day": day,
                "slots": slots.filter(start__gte=day, start__lt=day+datetime.timedelta(1))
                } )
        return days


class Slot(models.Model):
    room = models.ForeignKey(Room)
    start = models.DateTimeField()
    end = models.DateTimeField()
    base_price = PriceField()
    extra_person_price = PriceField()

    def save(self):
        # TODO look up other slots to see if there's a clash
        models.Model.save(self)

    def __unicode__(self):
        return u"%s (%i mins)" % (self.start.strftime(u'%a %x %H:%M'), (self.end - self.start).seconds / 60)

    objects = SlotManager()

class Customer(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=100, null=True)

# collection of bookings for a 
class Order(models.Model):
    customer = models.ForeignKey(Customer)
    status = models.CharField(max_length=30, choices=(("shopping", "Customer still shopping"), ("paying", "Customer paying"), ("paid", "Order paid and confirmed")))

    def save(self):
        if self.status == "paid":
            for booking in self.booking_set.all():
                booking.category = "paid"

        if self.status in ("shopping", "paying"):
            for booking in self.booking_set.all():
                booking.category = "reserved"

        models.Model.save(self)

# link order to slot
class Booking(models.Model):
    slot = models.OneToOneField(Slot)
    # a booking can be made without an order by an admin
    order = models.ForeignKey(Order, null=True)
    category = models.CharField(max_length=30, choices=(('paid', 'A paid for booking'), ('reserved', 'A held booking (while customer shops)'), ('suspended','A slot reserved staff'), ('cancellation', 'a previously booked slot that is available')))
    num_persons = models.IntegerField()

    # use to acertain when a held slot is expired
    date_booked = models.DateTimeField(default=datetime.datetime.now)

    customer_comments = models.TextField(null=True)
    admin_comments = models.TextField(null=True)

class PartyMember(models.Model):
    booking = models.ForeignKey(Booking)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    wants_internal_marketing = models.BooleanField(default=True, help_text="Is happy to receive internal marketing")

