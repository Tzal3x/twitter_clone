users = [
    {
        "username": "test_user_1",
        "first_name": "John",
        "last_name": "Doe",
        "birth": "1970-01-01",
        "email": "johndoe.avblr1751@mail.com",
        "phone_number": "003045454545",
        "password": "f*G(E14pa-osd.sda",
        "bio": "Just an ordinary person trying to navigate the complexities of life."
    },
    {
        "username": "test_user_2",
        # "first_name": "Emma",
        # "last_name": "Johnson",
        # "birth": "1985-04-15",
        "email": "emma.johnson543@mail.com",
        "phone_number": "004056787878",
        "password": "g&H)F36ma-lfpd.sda",
        # "bio": "Professional pizza eater and cat enthusiast."
    },
    {
        "username": "test_user_3",
        # "first_name": "Michael",
        # "last_name": "Smith",
        "birth": "1992-07-22",
        "email": "michael.smith456@mail.com",
        "phone_number": "005067895643",
        "password": "p@L(W19sm-oida.wap",
        "bio": "Lover of all things chocolate and a part-time superhero in training."
    },
    {
        "username": "test_user_4",
        "first_name": "Sophia",
        "last_name": "Williams",
        "birth": "1988-12-05",
        "email": "sophia.williams123@mail.com",
        "phone_number": "004056712345",
        "password": "k#S)D56wp-akoi.sda",
        # "bio": "Professional ice cream taster and expert daydreamer."
    },
    {
        "username": "test_user_5",
        "first_name": "Daniel",
        "last_name": "Brown",
        "birth": "1978-09-18",
        "email": "daniel.brown456@mail.com",
        "phone_number": "003046789012",
        "password": "a@M)F23br-olid.sda",
        "bio": "Adventurer, coffee lover, and occasional skydiver."
    },
    {
        "username": "test_user_6",
        "first_name": "Olivia",
        "last_name": "Taylor",
        # "birth": "1995-03-25",
        "email": "olivia.taylor789@mail.com",
        "phone_number": "004056743210",
        "password": "h&L)D49ta-rfwl.sda",
        "bio": "Bookworm, travel enthusiast, and professional napper."
    }
]


# TODO write tests so that the following users will fail to be created
invalid_create_users = [
    {
        # EMPTY-ON-PURPOSE
    },
    {
        "username": "invalid_test_user_1",
        "first_name": "David",
        "last_name": "Anderson",
        "birth": "1983-06-12",
        "email": "david.anderson234d.com", # Not an email
        "phone_number": "003047896543",
        "password": "",  # EMPTY Password/too short
        "bio": "Full-time pizza delivery guy and part-time ninja warrior."
    },
    {
        # "username": "invalid_test_user_2",  # NO USERNAME 
        "first_name": "Sophie",
        "last_name": "Martin",
        "birth": "1990-11-30",
        # "email": "sophie.martin789@mail.com",  # NO EMAIL
        # "phone_number": "004056798765",  # NO PHONE NUMBER
        # "password": "o&T)F56ma-pfsd.sda",  # NO PASSWORD
        "bio": "Coffee addict, music lover, and aspiring unicorn tamer." * 10  # TOO LONG BIO
    },
    {
        # "username": "invalid_test_user_1",
        "first_name": "James",
        "last_name": "Walker",
        "birth": "1975-08-08",
        "email": "jameswalker321mail.com",  # NOT AN EMAIL
        "phone_number": "003045671234",
        "password": "u&J)H28wa-omds.sda",
        "bio": "Professional procrastinator and master of witty comebacks."
    },
    {
        "username": "invalid_test_user_4",
        "first_name": "Ava" * 100, # TOO LONG STRING
        "last_name": "Clark", # TOO LONG STRING
        "birth": "3023-02-14",  # BIRTHDAY should not be in the future
        "email": "ava.clark567@mail.com",
        "phone_number": "004056765432004056765432004056765432",  # HUGE PHONE NUMBER
        "password": "e&R)K93cl-ahdf.sda" * 1000,  # TOO LONG STRING
        "bio": "Serial binge-watcher and champion of sleeping in on weekends."
    },
]
