# utils/choices.py (create this to store reusable choices)

EVENT_CHOICES = [
        ('wedding', 'Wedding'),
        ('burial', 'Burial/Funeral'),
        ('birthday', 'Birthday Party'),
        ('conference', 'Conference'),
        ('concert', 'Concert'),
        ('corporate', 'Corporate Event'),
        ('religious', 'Religious Event'),
        ('school', 'School/Campus Event'),
        ('private', 'Private Party'),
        ('entertainment', 'Entertainment'),
    ]



NIGERIAN_STATES = [
    ('abia', 'Abia'),
    ('adamawa', 'Adamawa'),
    ('akwa_ibom', 'Akwa Ibom'),
    ('anambra', 'Anambra'),
    ('bauchi', 'Bauchi'),
    ('bayelsa', 'Bayelsa'),
    ('benue', 'Benue'),
    ('borno', 'Borno'),
    ('cross_river', 'Cross River'),
    ('delta', 'Delta'),
    ('ebonyi', 'Ebonyi'),
    ('edo', 'Edo'),
    ('ekiti', 'Ekiti'),
    ('enugu', 'Enugu'),
    ('gombe', 'Gombe'),
    ('imo', 'Imo'),
    ('jigawa', 'Jigawa'),
    ('kaduna', 'Kaduna'),
    ('kano', 'Kano'),
    ('katsina', 'Katsina'),
    ('kebbi', 'Kebbi'),
    ('kogi', 'Kogi'),
    ('kwara', 'Kwara'),
    ('lagos', 'Lagos'),
    ('nasarawa', 'Nasarawa'),
    ('niger', 'Niger'),
    ('ogun', 'Ogun'),
    ('ondo', 'Ondo'),
    ('osun', 'Osun'),
    ('oyo', 'Oyo'),
    ('plateau', 'Plateau'),
    ('rivers', 'Rivers'),
    ('sokoto', 'Sokoto'),
    ('taraba', 'Taraba'),
    ('yobe', 'Yobe'),
    ('zamfara', 'Zamfara'),
    ('fct', 'FCT - Abuja'),
]

USER_TYPES = (
        ('usher', 'Usher'),
        ('host', 'Host'),
    )


STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )



PAYMENT_TYPES = (
    ('subscription', 'Subscription'),
    ('booking_fee', 'Booking Fee'),
    ('ticket', 'Ticket'),
)


PAYMENT_STATUS = (
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
)

EVENT_MODES = (
    ('ushering_only', 'Ushering_Only'),
    ('ticketing_only', 'Ticketing_Only'),
    ('ushering_and_ticketing', 'Ushering_And_Ticketing'),
)