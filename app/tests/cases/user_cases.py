users = [
    {
        "username": "test_user_1",
        "first_name": "John",
        "last_name": "Doe",
        "birth": "1970-01-01",
        "email": "johndoe.avblr1751@mail.com",
        "phone_number": "+306933395612", 
        "password": "f*G(E14pa-osd.sda",
        "bio": "Just an ordinary person trying to navigate the complexities of life."
    },
    {
        "username": "test_user_2",
        # "first_name": "Emma",
        # "last_name": "Johnson",
        "birth": "1985-04-15",
        "email": "emma.johnson543@mail.com",
        "phone_number": "+306940115079",
        "password": "g&H)F36ma-lfpd.sda",
        # "bio": "Professional pizza eater and cat enthusiast."
    },
    {
        "username": "test_user_3",
        # "first_name": "Michael",
        # "last_name": "Smith",
        "birth": "1992-07-22",
        "email": "michael.smith456@mail.com",
        "phone_number": "+306911195612",
        "password": "p@L(W19sm-oida.wap",
        "bio": "Lover of all things chocolate and a part-time superhero in training."
    },
    {
        "username": "test_user_4",
        "first_name": "Sophia",
        "last_name": "Williams",
        "birth": "1988-12-05",
        "email": "sophia.williams123@mail.com",
        "phone_number": "+306933399999",
        "password": "k#S)D56wp-akoi.sda",
        # "bio": "Professional ice cream taster and expert daydreamer."
    },
    {
        "username": "test_user_5",
        "first_name": "Daniel",
        "last_name": "Brown",
        "birth": "1978-09-18",
        "email": "daniel.brown456@mail.com",
        "phone_number": "+306969395612",
        "password": "a@M)F23br-olid.sda",
        "bio": "Adventurer, coffee lover, and occasional skydiver."
    },
    {
        "username": "test_user_6",
        # "first_name": "Olivia",
        # "last_name": "Taylor",
        "birth": "1995-03-25",
        "email": "olivia.taylor789@mail.com",
        "phone_number": "+306933395612",
        "password": "h&L)D49ta-rfwl.sda",
        # "bio": "Bookworm, travel enthusiast, and professional napper."
    }
]


"""
Those users are not supposed to become database entries.
They are supposed to fail on purpose on the creation step,
because they have invalid or missing fields that are required.
"""
invalid_registration_users = [
    {
        "username": "s",
        "birth": "1983-06-12",
        "email": "david@email.com",
        "phone_number": "+303933395332",
        "password": "h&L)D49ta-rfwl.sda"
    },
    {
        "username": "weak_password",
        "birth": "1983-06-12",
        "email": "david@gmail.com",
        "phone_number": "+306933395612",
        "password": "h"
    },
    {
        "username": "invalid_phone_number",
        "birth": "1983-06-12",
        "email": "david@gmail.com",
        "phone_number": "+300003933395332",
        "password": "h"
    },
    {
        "username": "invalid_test_user",
        "birth": "1983-06-12",
        "email": "david.anderson234d.com",  # Not an email
        "phone_number": "+303933395332",
        "password": "h&L)D49ta-rfwl.sda"
    },
    {
        "username": "invalid_test_user",
        "first_name": "James",
        "last_name": "Walker",
        "birth": "1975-08-08",
        "email": "jameswalker321mail.com",  # NOT a valid email
        "phone_number": "+003045671234",
        "password": "u&J)H28wa-omds.sda",
        "bio": "Professional procrastinator and master of witty comebacks."
    },
    {
        "username": "future_birthday",
        "first_name": "Ava",
        "last_name": "Clark",
        "birth": "3023-02-14",  # BIRTHDAY should not be in the future
        "email": "ava.clark567@mail.com",
        "phone_number": "+303933395332123",
        "password": "e&R)K93cl-ahdf.sda",
        "bio": "Serial binge-watcher and champion of sleeping in on weekends."
    },
    {
        "username": "invalid_test_user",
        "first_name": "Ava",
        "last_name": "Clark",
        "birth": "1980-02-14",
        "email": "ava.clark567@mail.com",
        "phone_number": "004056765432004056765432004056765432",  # HUGE PHONE NUMBER
        "password": "e&R)K93cl-ahdf.sda",
        "bio": "Serial binge-watcher and champion of sleeping in on weekends."
    },
    {
        "username": "invalid_test_user",
        "first_name": "Ava",
        "last_name": "Clark",
        "birth": "1998-02-14",
        "email": "ava.clark567@mail.com",
        "phone_number": "a000000000",  # Not a phone number
        "password": "e&R)K93cl-ahdf.sda",
        "bio": "Serial binge-watcher and champion of sleeping in on weekends."
    },
]
