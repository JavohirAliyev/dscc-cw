"""
Django management command to seed the database with initial data
Usage: python manage.py seed_database
"""
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from library.models import Author, Category, Book, BorrowRecord, UserProfile


class Command(BaseCommand):
    help = 'Seeds the database with initial data: 200 books, authors, categories, users, and borrow records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            BorrowRecord.objects.all().delete()
            Book.objects.all().delete()
            Category.objects.all().delete()
            Author.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Seed Categories
        self.stdout.write('Creating categories...')
        categories = self.create_categories()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(categories)} categories'))

        # Seed Authors
        self.stdout.write('Creating authors...')
        authors = self.create_authors()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(authors)} authors'))

        # Seed Books
        self.stdout.write('Creating books...')
        books = self.create_books(authors, categories)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(books)} books'))

        # Seed Users
        self.stdout.write('Creating users...')
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))

        # Seed Borrow Records
        self.stdout.write('Creating borrow records...')
        records = self.create_borrow_records(users, books)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(records)} borrow records'))

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Summary:')
        self.stdout.write(f'  - Categories: {len(categories)}')
        self.stdout.write(f'  - Authors: {len(authors)}')
        self.stdout.write(f'  - Books: {len(books)}')
        self.stdout.write(f'  - Users: {len(users)}')
        self.stdout.write(f'  - Borrow Records: {len(records)}')

    def create_categories(self):
        """Create book categories"""
        categories_data = [
            ('Fiction', 'Narrative prose literary works'),
            ('Non-Fiction', 'Factual and informative books'),
            ('Science Fiction', 'Speculative fiction with futuristic themes'),
            ('Fantasy', 'Magic and supernatural elements'),
            ('Mystery', 'Detective and crime stories'),
            ('Thriller', 'Suspenseful and exciting narratives'),
            ('Romance', 'Love stories and relationships'),
            ('Horror', 'Scary and frightening tales'),
            ('Biography', 'Life stories of real people'),
            ('History', 'Historical events and periods'),
            ('Science', 'Scientific knowledge and discoveries'),
            ('Technology', 'Computing and technological advances'),
            ('Business', 'Business and entrepreneurship'),
            ('Self-Help', 'Personal development and improvement'),
            ('Philosophy', 'Philosophical thoughts and theories'),
            ('Psychology', 'Human behavior and mental processes'),
            ('Art', 'Visual arts and creativity'),
            ('Poetry', 'Poetic works and collections'),
            ('Drama', 'Theatrical and dramatic works'),
            ('Children', 'Books for young readers'),
        ]

        categories = []
        for name, description in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            categories.append(category)

        return categories

    def create_authors(self):
        """Create 60 diverse authors"""
        authors_data = [
            # Classic Authors
            ('William Shakespeare', 'English playwright and poet', '1564-04-23', 'English'),
            ('Jane Austen', 'English novelist known for romantic fiction', '1775-12-16', 'English'),
            ('Charles Dickens', 'Victorian era novelist', '1812-02-07', 'English'),
            ('Leo Tolstoy', 'Russian author of War and Peace', '1828-09-09', 'Russian'),
            ('Fyodor Dostoevsky', 'Russian novelist and philosopher', '1821-11-11', 'Russian'),
            ('Mark Twain', 'American author and humorist', '1835-11-30', 'American'),
            ('Ernest Hemingway', 'American novelist and journalist', '1899-07-21', 'American'),
            ('F. Scott Fitzgerald', 'Jazz Age writer', '1896-09-24', 'American'),
            ('Virginia Woolf', 'Modernist English writer', '1882-01-25', 'English'),
            ('James Joyce', 'Irish modernist writer', '1882-02-02', 'Irish'),
            
            # Modern Fiction
            ('Gabriel García Márquez', 'Colombian novelist, magical realism', '1927-03-06', 'Colombian'),
            ('Toni Morrison', 'American novelist, Nobel laureate', '1931-02-18', 'American'),
            ('Haruki Murakami', 'Japanese contemporary writer', '1949-01-12', 'Japanese'),
            ('Margaret Atwood', 'Canadian author and poet', '1939-11-18', 'Canadian'),
            ('Salman Rushdie', 'British Indian novelist', '1947-06-19', 'British-Indian'),
            ('Isabel Allende', 'Chilean-American writer', '1942-08-02', 'Chilean'),
            ('Paulo Coelho', 'Brazilian lyricist and novelist', '1947-08-24', 'Brazilian'),
            ('Chimamanda Ngozi Adichie', 'Nigerian novelist', '1977-09-15', 'Nigerian'),
            ('Kazuo Ishiguro', 'British novelist', '1954-11-08', 'British-Japanese'),
            ('Don DeLillo', 'American postmodern author', '1936-11-20', 'American'),
            
            # Science Fiction & Fantasy
            ('J.R.R. Tolkien', 'Author of The Lord of the Rings', '1892-01-03', 'English'),
            ('George Orwell', 'Author of 1984 and Animal Farm', '1903-06-25', 'English'),
            ('Isaac Asimov', 'Science fiction writer and biochemist', '1920-01-02', 'American'),
            ('Arthur C. Clarke', 'British science fiction writer', '1917-12-16', 'British'),
            ('Ursula K. Le Guin', 'Fantasy and science fiction author', '1929-10-21', 'American'),
            ('Philip K. Dick', 'Science fiction writer', '1928-12-16', 'American'),
            ('Ray Bradbury', 'Author of Fahrenheit 451', '1920-08-22', 'American'),
            ('Frank Herbert', 'Author of Dune', '1920-10-08', 'American'),
            ('Neil Gaiman', 'English fantasy author', '1960-11-10', 'English'),
            ('Brandon Sanderson', 'Epic fantasy writer', '1975-12-19', 'American'),
            
            # Mystery & Thriller
            ('Agatha Christie', 'Queen of mystery novels', '1890-09-15', 'English'),
            ('Arthur Conan Doyle', 'Creator of Sherlock Holmes', '1859-05-22', 'Scottish'),
            ('Stephen King', 'Master of horror fiction', '1947-09-21', 'American'),
            ('Dan Brown', 'Author of The Da Vinci Code', '1964-06-22', 'American'),
            ('Gillian Flynn', 'Author of Gone Girl', '1971-02-24', 'American'),
            ('John Grisham', 'Legal thriller writer', '1955-02-08', 'American'),
            ('Lee Child', 'British thriller writer', '1954-10-29', 'British'),
            ('Patricia Highsmith', 'American psychological thriller writer', '1921-01-19', 'American'),
            
            # Non-Fiction & Biography
            ('Malcolm Gladwell', 'Canadian journalist and author', '1963-09-03', 'Canadian'),
            ('Yuval Noah Harari', 'Israeli historian', '1976-02-24', 'Israeli'),
            ('Michelle Obama', 'Former First Lady and author', '1964-01-17', 'American'),
            ('Walter Isaacson', 'Biographer and journalist', '1952-05-20', 'American'),
            ('Doris Kearns Goodwin', 'American historian', '1943-01-04', 'American'),
            ('David McCullough', 'American historian and author', '1933-07-07', 'American'),
            
            # Philosophy & Psychology
            ('Carl Jung', 'Swiss psychiatrist and psychoanalyst', '1875-07-26', 'Swiss'),
            ('Sigmund Freud', 'Founder of psychoanalysis', '1856-05-06', 'Austrian'),
            ('Viktor Frankl', 'Austrian neurologist and psychiatrist', '1905-03-26', 'Austrian'),
            ('Daniel Kahneman', 'Psychologist and economist', '1934-03-05', 'Israeli-American'),
            ('Jordan Peterson', 'Canadian clinical psychologist', '1962-06-12', 'Canadian'),
            
            # Contemporary Fiction
            ('Colleen Hoover', 'Contemporary romance author', '1979-12-11', 'American'),
            ('John Green', 'Young adult fiction writer', '1977-08-24', 'American'),
            ('Celeste Ng', 'American novelist', '1980-07-30', 'American'),
            ('Taylor Jenkins Reid', 'Contemporary fiction author', '1983-12-20', 'American'),
            ('Fredrik Backman', 'Swedish writer', '1981-06-02', 'Swedish'),
            ('Elena Ferrante', 'Pseudonymous Italian novelist', '1943-04-15', 'Italian'),
            ('Sally Rooney', 'Irish novelist', '1991-02-20', 'Irish'),
            ('Madeline Miller', 'American novelist', '1978-07-24', 'American'),
            ('Ruth Ware', 'British psychological thriller author', '1977-11-02', 'British'),
            ('Delia Owens', 'American author and zoologist', '1949-04-04', 'American'),
        ]

        authors = []
        for name, bio, birth_date, nationality in authors_data:
            author, created = Author.objects.get_or_create(
                name=name,
                defaults={
                    'bio': bio,
                    'birth_date': datetime.strptime(birth_date, '%Y-%m-%d').date(),
                    'nationality': nationality
                }
            )
            authors.append(author)

        return authors

    def create_books(self, authors, categories):
        """Create 200 books with diverse titles"""
        books_data = [
            # Classic Literature
            ('Pride and Prejudice', 'Jane Austen', '9780141439518', 'A romantic novel of manners', '1813-01-28', 432),
            ('1984', 'George Orwell', '9780451524935', 'Dystopian social science fiction', '1949-06-08', 328),
            ('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'Coming-of-age story in the American South', '1960-07-11', 324),
            ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Tragic story of Jay Gatsby', '1925-04-10', 180),
            ('War and Peace', 'Leo Tolstoy', '9780199232765', 'Epic tale of Russian society', '1869-01-01', 1225),
            ('Crime and Punishment', 'Fyodor Dostoevsky', '9780486415871', 'Psychological novel about morality', '1866-01-01', 671),
            ('Moby-Dick', 'Herman Melville', '9781503280786', 'The voyage of Captain Ahab', '1851-10-18', 585),
            ('Jane Eyre', 'Charlotte Brontë', '9780142437209', 'Story of an orphaned governess', '1847-10-16', 532),
            ('Wuthering Heights', 'Emily Brontë', '9780141439556', 'Gothic tale of passion', '1847-12-01', 416),
            ('The Catcher in the Rye', 'J.D. Salinger', '9780316769174', 'Teenage rebellion and angst', '1951-07-16', 277),
            
            # Modern Literature
            ('One Hundred Years of Solitude', 'Gabriel García Márquez', '9780060883287', 'Multi-generational family saga', '1967-05-30', 417),
            ('Beloved', 'Toni Morrison', '9781400033416', 'Story of a former slave', '1987-09-16', 324),
            ('Norwegian Wood', 'Haruki Murakami', '9780375704024', 'Coming-of-age love story', '1987-09-04', 296),
            ('The Handmaid\'s Tale', 'Margaret Atwood', '9780385490818', 'Dystopian feminist novel', '1985-06-17', 311),
            ('Midnight\'s Children', 'Salman Rushdie', '9780812976533', 'Magical realism about India', '1981-04-18', 647),
            ('The House of the Spirits', 'Isabel Allende', '9781501117015', 'Multi-generational Chilean family', '1982-01-01', 448),
            ('The Alchemist', 'Paulo Coelho', '9780062315007', 'Philosophical tale of self-discovery', '1988-01-01', 208),
            ('Half of a Yellow Sun', 'Chimamanda Ngozi Adichie', '9781400095209', 'Nigerian Civil War story', '2006-09-12', 433),
            ('Never Let Me Go', 'Kazuo Ishiguro', '9781400078776', 'Dystopian science fiction', '2005-02-14', 288),
            ('White Noise', 'Don DeLillo', '9780143105985', 'Postmodern American life', '1985-01-01', 326),
            
            # Fantasy & Epic Fiction
            ('The Lord of the Rings', 'J.R.R. Tolkien', '9780544003415', 'Epic high fantasy adventure', '1954-07-29', 1178),
            ('The Hobbit', 'J.R.R. Tolkien', '9780547928227', 'Fantasy adventure of Bilbo Baggins', '1937-09-21', 310),
            ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', '9780439708180', 'Boy wizard discovers his destiny', '1997-06-26', 309),
            ('A Game of Thrones', 'George R.R. Martin', '9780553593716', 'Epic fantasy political intrigue', '1996-08-06', 694),
            ('The Name of the Wind', 'Patrick Rothfuss', '9780756404741', 'Tale of legendary figure Kvothe', '2007-03-27', 662),
            ('The Way of Kings', 'Brandon Sanderson', '9780765326355', 'Epic fantasy Stormlight Archive', '2010-08-31', 1007),
            ('Mistborn: The Final Empire', 'Brandon Sanderson', '9780765350381', 'Heist in a dystopian fantasy world', '2006-07-17', 541),
            ('American Gods', 'Neil Gaiman', '9780380789030', 'Modern fantasy mythology', '2001-06-19', 465),
            ('The Left Hand of Darkness', 'Ursula K. Le Guin', '9780441478125', 'Science fiction gender exploration', '1969-03-01', 304),
            ('A Wizard of Earthsea', 'Ursula K. Le Guin', '9780547773742', 'Coming-of-age fantasy story', '1968-11-01', 183),
            
            # Science Fiction
            ('Dune', 'Frank Herbert', '9780441172719', 'Epic space opera about desert planet', '1965-06-01', 688),
            ('Foundation', 'Isaac Asimov', '9780553293357', 'Galactic empire and psychohistory', '1951-06-01', 255),
            ('2001: A Space Odyssey', 'Arthur C. Clarke', '9780451457998', 'Space exploration and AI', '1968-06-16', 297),
            ('Do Androids Dream of Electric Sheep?', 'Philip K. Dick', '9780345404473', 'Bounty hunter hunts androids', '1968-01-01', 210),
            ('Fahrenheit 451', 'Ray Bradbury', '9781451673319', 'Book burning dystopia', '1953-10-19', 249),
            ('The Martian', 'Andy Weir', '9780553418026', 'Astronaut stranded on Mars', '2011-01-01', 387),
            ('Ender\'s Game', 'Orson Scott Card', '9780812550702', 'Child military genius', '1985-01-15', 324),
            ('Neuromancer', 'William Gibson', '9780441569595', 'Cyberpunk hacking thriller', '1984-07-01', 271),
            ('The Time Machine', 'H.G. Wells', '9780486284729', 'Time travel to distant future', '1895-01-01', 118),
            ('Brave New World', 'Aldous Huxley', '9780060850524', 'Dystopian genetically modified society', '1932-01-01', 268),
            
            # Mystery & Thriller
            ('Murder on the Orient Express', 'Agatha Christie', '9780062693662', 'Hercule Poirot investigates', '1934-01-01', 256),
            ('The Hound of the Baskervilles', 'Arthur Conan Doyle', '9780451528018', 'Sherlock Holmes mystery', '1902-04-01', 256),
            ('The Shining', 'Stephen King', '9780385528856', 'Horror in an isolated hotel', '1977-01-28', 447),
            ('The Da Vinci Code', 'Dan Brown', '9780307474278', 'Religious conspiracy thriller', '2003-03-18', 489),
            ('Gone Girl', 'Gillian Flynn', '9780307588371', 'Psychological thriller about marriage', '2012-06-05', 422),
            ('The Girl with the Dragon Tattoo', 'Stieg Larsson', '9780307454546', 'Swedish crime thriller', '2005-08-01', 465),
            ('The Silence of the Lambs', 'Thomas Harris', '9780312195267', 'FBI agent and serial killer', '1988-10-01', 338),
            ('Big Little Lies', 'Liane Moriarty', '9780399167065', 'Mystery in suburban community', '2014-07-29', 460),
            ('The Woman in the Window', 'A.J. Finn', '9780062678416', 'Agoraphobic woman witnesses crime', '2018-01-02', 427),
            ('In Cold Blood', 'Truman Capote', '9780679745587', 'True crime account', '1966-01-01', 343),
            
            # Contemporary Fiction
            ('The Fault in Our Stars', 'John Green', '9780142424179', 'Teenage cancer patients fall in love', '2012-01-10', 313),
            ('It Ends with Us', 'Colleen Hoover', '9781501110368', 'Romance with domestic violence themes', '2016-08-02', 384),
            ('Where the Crawdads Sing', 'Delia Owens', '9780735219090', 'Coming-of-age mystery in marshlands', '2018-08-14', 370),
            ('Little Fires Everywhere', 'Celeste Ng', '9780735224315', 'Suburban family drama', '2017-09-12', 338),
            ('The Seven Husbands of Evelyn Hugo', 'Taylor Jenkins Reid', '9781501139239', 'Hollywood actress tells her story', '2017-06-13', 388),
            ('A Man Called Ove', 'Fredrik Backman', '9781476738024', 'Curmudgeon finds purpose', '2012-08-27', 337),
            ('Normal People', 'Sally Rooney', '9781984822178', 'Irish coming-of-age romance', '2018-08-28', 273),
            ('The Midnight Library', 'Matt Haig', '9780525559474', 'Parallel lives exploration', '2020-08-13', 304),
            ('Circe', 'Madeline Miller', '9780316556347', 'Greek mythology retelling', '2018-04-10', 393),
            ('The Silent Patient', 'Alex Michaelides', '9781250301697', 'Psychological thriller', '2019-02-05', 325),
            
            # Historical Fiction
            ('All the Light We Cannot See', 'Anthony Doerr', '9781501173219', 'WWII story of blind French girl', '2014-05-06', 531),
            ('The Book Thief', 'Markus Zusak', '9780375842207', 'Nazi Germany through Death\'s eyes', '2005-09-01', 552),
            ('The Nightingale', 'Kristin Hannah', '9781250080400', 'Two sisters in occupied France', '2015-02-03', 440),
            ('Wolf Hall', 'Hilary Mantel', '9780312429980', 'Thomas Cromwell in Tudor England', '2009-10-06', 604),
            ('The Pillars of the Earth', 'Ken Follett', '9780451488336', 'Cathedral building in Middle Ages', '1989-10-01', 973),
            ('Lonesome Dove', 'Larry McMurtry', '9781439195260', 'Epic Western cattle drive', '1985-06-01', 843),
            ('The Help', 'Kathryn Stockett', '9780425245132', '1960s Mississippi domestic workers', '2009-02-10', 451),
            ('Memoirs of a Geisha', 'Arthur Golden', '9780375714856', 'Life of Japanese geisha', '1997-09-01', 434),
            
            # Non-Fiction & Biography
            ('Sapiens', 'Yuval Noah Harari', '9780062316110', 'Brief history of humankind', '2011-01-01', 443),
            ('Educated', 'Tara Westover', '9780399590504', 'Memoir of Mormon survivalist family', '2018-02-20', 334),
            ('Becoming', 'Michelle Obama', '9781524763138', 'Memoir of former First Lady', '2018-11-13', 426),
            ('Steve Jobs', 'Walter Isaacson', '9781501127625', 'Biography of Apple founder', '2011-10-24', 656),
            ('The Immortal Life of Henrietta Lacks', 'Rebecca Skloot', '9781400052189', 'Story of HeLa cells', '2010-02-02', 381),
            ('Thinking, Fast and Slow', 'Daniel Kahneman', '9780374533557', 'Psychology of decision-making', '2011-10-25', 499),
            ('The Power of Habit', 'Charles Duhigg', '9780812981605', 'Science of habit formation', '2012-02-28', 371),
            ('Atomic Habits', 'James Clear', '9780735211292', 'Building better habits', '2018-10-16', 320),
            ('Man\'s Search for Meaning', 'Viktor Frankl', '9780807014295', 'Holocaust survival and logotherapy', '1946-01-01', 184),
            ('The Subtle Art of Not Giving a F*ck', 'Mark Manson', '9780062457714', 'Counterintuitive life advice', '2016-09-13', 224),
            
            # Business & Self-Help
            ('How to Win Friends and Influence People', 'Dale Carnegie', '9780671027032', 'Classic self-improvement', '1936-10-01', 288),
            ('Rich Dad Poor Dad', 'Robert Kiyosaki', '9781612680194', 'Financial education and wealth', '1997-04-01', 336),
            ('The 7 Habits of Highly Effective People', 'Stephen Covey', '9781982137274', 'Personal effectiveness principles', '1989-08-15', 381),
            ('Good to Great', 'Jim Collins', '9780066620992', 'Why companies make the leap', '2001-10-16', 300),
            ('Start with Why', 'Simon Sinek', '9781591846444', 'Inspirational leadership', '2009-10-29', 256),
            ('The Lean Startup', 'Eric Ries', '9780307887894', 'Innovation methodology', '2011-09-13', 336),
            ('Zero to One', 'Peter Thiel', '9780804139298', 'Notes on startups', '2014-09-16', 224),
            ('Dare to Lead', 'Brené Brown', '9780399592522', 'Brave work and tough conversations', '2018-10-09', 320),
            
            # Science & Technology
            ('A Brief History of Time', 'Stephen Hawking', '9780553380163', 'Cosmology for general readers', '1988-04-01', 256),
            ('The Selfish Gene', 'Richard Dawkins', '9780198788607', 'Gene-centered evolution', '1976-01-01', 360),
            ('Cosmos', 'Carl Sagan', '9780345539434', 'Universe exploration', '1980-01-01', 365),
            ('The Code Breaker', 'Walter Isaacson', '9781982115852', 'Jennifer Doudna and gene editing', '2021-03-09', 560),
            ('The Innovators', 'Walter Isaacson', '9781476708706', 'Digital revolution history', '2014-10-07', 542),
            ('The Soul of a New Machine', 'Tracy Kidder', '9780316491976', 'Computer engineering story', '1981-08-01', 293),
            
            # Philosophy
            ('Meditations', 'Marcus Aurelius', '9780812968255', 'Stoic philosophy reflections', '0180-01-01', 254),
            ('The Republic', 'Plato', '9780872201361', 'Socratic dialogue on justice', '-0380-01-01', 416),
            ('Beyond Good and Evil', 'Friedrich Nietzsche', '9780679724650', 'Critique of traditional morality', '1886-01-01', 260),
            ('The Stranger', 'Albert Camus', '9780679720201', 'Existentialist novel', '1942-01-01', 123),
            ('Being and Time', 'Martin Heidegger', '9780061575594', 'Phenomenological ontology', '1927-01-01', 589),
            
            # Poetry & Drama
            ('The Complete Works of William Shakespeare', 'William Shakespeare', '9780517053614', 'All plays and sonnets', '1623-01-01', 1232),
            ('Paradise Lost', 'John Milton', '9780140424393', 'Epic poem about the Fall', '1667-01-01', 453),
            ('The Waste Land', 'T.S. Eliot', '9780156948890', 'Modernist poetry', '1922-01-01', 88),
            ('Leaves of Grass', 'Walt Whitman', '9780143106494', 'American poetry collection', '1855-07-04', 624),
            
            # Children's & Young Adult
            ('Charlotte\'s Web', 'E.B. White', '9780064400558', 'Story of friendship on a farm', '1952-10-15', 192),
            ('The Chronicles of Narnia', 'C.S. Lewis', '9780066238500', 'Fantasy series for children', '1950-10-16', 767),
            ('Matilda', 'Roald Dahl', '9780142410370', 'Girl with telekinetic powers', '1988-10-01', 240),
            ('The Hunger Games', 'Suzanne Collins', '9780439023528', 'Dystopian survival competition', '2008-09-14', 374),
            ('Percy Jackson & The Lightning Thief', 'Rick Riordan', '9780786838653', 'Modern Greek mythology adventure', '2005-07-01', 377),
            ('Wonder', 'R.J. Palacio', '9780375869020', 'Boy with facial differences', '2012-02-14', 310),
            
            # Horror
            ('Dracula', 'Bram Stoker', '9780486411095', 'Classic vampire novel', '1897-05-26', 418),
            ('Frankenstein', 'Mary Shelley', '9780486282114', 'Gothic science fiction horror', '1818-01-01', 280),
            ('It', 'Stephen King', '9781501142970', 'Terrifying entity haunts children', '1986-09-15', 1138),
            ('The Exorcist', 'William Peter Blatty', '9780061007224', 'Demonic possession horror', '1971-01-01', 385),
            ('Bird Box', 'Josh Malerman', '9780062259653', 'Post-apocalyptic horror', '2014-05-13', 262),
            
            # Romance
            ('Outlander', 'Diana Gabaldon', '9780440212560', 'Time travel historical romance', '1991-06-01', 627),
            ('Me Before You', 'Jojo Moyes', '9780143124542', 'Caregiver falls for quadriplegic', '2012-01-05', 369),
            ('The Notebook', 'Nicholas Sparks', '9780446676090', 'Enduring love story', '1996-10-01', 214),
            ('Beach Read', 'Emily Henry', '9781984806734', 'Contemporary romance writers', '2020-05-19', 361),
            ('Red, White & Royal Blue', 'Casey McQuiston', '9781250316776', 'LGBTQ+ political romance', '2019-05-14', 421),
            
            # Graphic Novels & Comics
            ('Watchmen', 'Alan Moore', '9781779501127', 'Deconstructionist superhero story', '1987-01-01', 448),
            ('Maus', 'Art Spiegelman', '9780679406419', 'Holocaust graphic novel', '1991-01-01', 296),
            ('Persepolis', 'Marjane Satrapi', '9780375714573', 'Memoir of Iranian Revolution', '2000-01-01', 153),
            ('V for Vendetta', 'Alan Moore', '9781401207922', 'Dystopian political thriller', '1988-01-01', 296),
            ('Sandman Vol. 1', 'Neil Gaiman', '9781401225759', 'Fantasy comic series', '1989-01-01', 240),
            
            # Adventure
            ('The Adventures of Huckleberry Finn', 'Mark Twain', '9780486280615', 'Mississippi River adventure', '1884-12-10', 366),
            ('Robinson Crusoe', 'Daniel Defoe', '9780141439822', 'Castaway survival story', '1719-04-25', 320),
            ('Treasure Island', 'Robert Louis Stevenson', '9780141321004', 'Pirates and treasure hunt', '1883-11-14', 240),
            ('The Count of Monte Cristo', 'Alexandre Dumas', '9780140449266', 'Revenge and adventure', '1844-08-28', 1276),
            ('Around the World in Eighty Days', 'Jules Verne', '9780486411118', 'Race around the globe', '1873-01-30', 212),
            ('Journey to the Center of the Earth', 'Jules Verne', '9780486440880', 'Underground expedition', '1864-11-25', 183),
            ('Twenty Thousand Leagues Under the Sea', 'Jules Verne', '9780143106470', 'Submarine adventure', '1870-06-20', 427),
            
            # Memoir & Essays
            ('The Diary of a Young Girl', 'Anne Frank', '9780553296983', 'Holocaust diary', '1947-06-25', 283),
            ('I Know Why the Caged Bird Sings', 'Maya Angelou', '9780345514400', 'Coming-of-age memoir', '1969-01-01', 289),
            ('Wild', 'Cheryl Strayed', '9780307476074', 'Pacific Crest Trail memoir', '2012-03-20', 315),
            ('Eat, Pray, Love', 'Elizabeth Gilbert', '9780143038412', 'Journey of self-discovery', '2006-02-16', 352),
            ('When Breath Becomes Air', 'Paul Kalanithi', '9780812988406', 'Neurosurgeon faces terminal cancer', '2016-01-12', 256),
            ('Born a Crime', 'Trevor Noah', '9780399588174', 'Growing up in apartheid South Africa', '2016-11-15', 304),
            
            # Additional Contemporary & Diverse
            ('The Kite Runner', 'Khaled Hosseini', '9781594631931', 'Friendship in Afghanistan', '2003-05-29', 371),
            ('A Thousand Splendid Suns', 'Khaled Hosseini', '9781594489501', 'Two women in Afghanistan', '2007-05-22', 372),
            ('Life of Pi', 'Yann Martel', '9780156027328', 'Boy survives with tiger on lifeboat', '2001-09-11', 319),
            ('The Joy Luck Club', 'Amy Tan', '9780143038092', 'Chinese-American mother-daughter stories', '1989-01-01', 288),
            ('Homegoing', 'Yaa Gyasi', '9781101971062', 'Multi-generational African diaspora', '2016-06-07', 305),
            ('The Underground Railroad', 'Colson Whitehead', '9780385542364', 'Slavery escape via literal railroad', '2016-08-02', 306),
            ('Pachinko', 'Min Jin Lee', '9781455563937', 'Korean family in Japan', '2017-02-07', 490),
            ('The God of Small Things', 'Arundhati Roy', '9780812979657', 'Twins in India', '1997-04-04', 340),
            ('Things Fall Apart', 'Chinua Achebe', '9780385474542', 'Pre-colonial Nigerian life', '1958-06-17', 209),
            ('Blindness', 'José Saramago', '9780156007757', 'Epidemic of blindness', '1995-10-01', 326),
        ]

        # Generate ISBN if needed and create books
        books = []
        used_isbns = set()
        
        for i, (title, author_name, isbn, description, pub_date, pages) in enumerate(books_data):
            # Find the author
            try:
                author = next(a for a in authors if a.name == author_name)
            except StopIteration:
                # If author not found, pick a random one
                author = random.choice(authors)
            
            # Ensure unique ISBN
            while isbn in used_isbns:
                # Generate a new ISBN by modifying the last digit
                isbn = isbn[:-1] + str(random.randint(0, 9))
            used_isbns.add(isbn)
            
            # Parse publication date
            try:
                pub_date_obj = datetime.strptime(pub_date, '%Y-%m-%d').date()
            except:
                pub_date_obj = datetime(2000, 1, 1).date()
            
            # Create book
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'author': author,
                    'description': description,
                    'publication_date': pub_date_obj,
                    'pages': pages,
                    'available_copies': random.randint(1, 10),
                    'total_copies': random.randint(5, 15),
                }
            )
            
            # Assign random categories (1-3 categories per book)
            num_categories = random.randint(1, 3)
            book_categories = random.sample(categories, num_categories)
            book.categories.set(book_categories)
            
            books.append(book)

        # If we need more books to reach 200, generate additional ones
        target_books = 200
        if len(books) < target_books:
            self.stdout.write(f'Generating {target_books - len(books)} additional books...')
            
            # Additional book titles for variety
            additional_titles = [
                'The Midnight Garden', 'Echoes of Tomorrow', 'The Last Symphony',
                'Whispers in the Dark', 'The Crimson Crown', 'Beneath the Silver Moon',
                'The Forgotten Kingdom', 'Dance of Shadows', 'The Crystal Empire',
                'Songs of the Deep', 'The Emerald Throne', 'Voices in the Mist',
                'The Golden Hour', 'Tales of the Wanderer', 'The Sapphire Sea',
                'Dreams of Tomorrow', 'The Iron Tower', 'Legends of the Past',
                'The Obsidian Gate', 'Chronicles of the North', 'The Diamond Path',
                'Secrets of the Ocean', 'The Ruby Sword', 'Mysteries of Time',
                'The Pearl Kingdom', 'Warriors of Light', 'The Amber Forest',
                'Stories of Courage', 'The Jade Mountain', 'Heroes of Legend',
                'The Silver Dagger', 'Paths of Destiny', 'The Bronze Shield',
                'Memories of Home', 'The Ivory Palace', 'Journeys Unknown',
                'The Platinum Ring', 'Adventures Await', 'The Copper Crown',
                'Worlds Beyond', 'The Steel Fortress', 'Dreams and Nightmares',
                'The Titanium Blade', 'Quest for Truth', 'The Marble Temple',
                'Horizons Unlimited', 'The Granite Keep', 'Endless Possibilities',
                'The Quartz Castle', 'New Beginnings', 'The Sandstone Palace',
                'Future Visions', 'The Limestone Tower', 'Hidden Treasures',
                'The Obsidian Mirror', 'Timeless Tales', 'The Onyx Medallion',
            ]
            
            genres = ['Adventure', 'Mystery', 'Romance', 'Thriller', 'Fantasy',
                     'Science Fiction', 'Historical', 'Contemporary']
            
            current_count = len(books)
            for i in range(current_count, target_books):
                # Cycle through additional titles or generate new ones
                if i - current_count < len(additional_titles):
                    title = additional_titles[i - current_count]
                else:
                    title = f"{random.choice(genres)} Story {i - current_count + 1}"
                
                author = random.choice(authors)
                
                # Generate unique ISBN
                isbn = f"97804{random.randint(10000000, 99999999)}"
                while isbn in used_isbns:
                    isbn = f"97804{random.randint(10000000, 99999999)}"
                used_isbns.add(isbn)
                
                # Generate publication date
                pub_date = datetime(
                    random.randint(1950, 2024),
                    random.randint(1, 12),
                    random.randint(1, 28)
                ).date()
                
                # Create book
                book = Book.objects.create(
                    title=title,
                    author=author,
                    isbn=isbn,
                    description=f"A captivating {random.choice(genres).lower()} novel that will keep you engaged from start to finish.",
                    publication_date=pub_date,
                    pages=random.randint(150, 600),
                    available_copies=random.randint(1, 10),
                    total_copies=random.randint(5, 15),
                )
                
                # Assign random categories
                num_categories = random.randint(1, 3)
                book_categories = random.sample(categories, num_categories)
                book.categories.set(book_categories)
                
                books.append(book)

        return books

    def create_users(self):
        """Create 25 regular users with profiles"""
        first_names = [
            'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
            'Isabella', 'William', 'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia',
            'Lucas', 'Harper', 'Henry', 'Evelyn', 'Alexander', 'Abigail', 'Michael',
            'Emily', 'Daniel', 'Elizabeth'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
            'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
            'Lee', 'Perez', 'Thompson', 'White', 'Harris'
        ]

        users = []
        for i in range(25):
            first_name = first_names[i]
            last_name = last_names[i]
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{username}@example.com"
            
            # Create user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            
            if created:
                user.set_password('password123')  # Set a default password
                user.save()
            
            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': f"+1-555-{random.randint(1000, 9999):04d}",
                    'address': f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Pine'])} St, City {random.randint(10, 99)}",
                    'date_of_birth': datetime(
                        random.randint(1960, 2005),
                        random.randint(1, 12),
                        random.randint(1, 28)
                    ).date(),
                }
            )
            
            users.append(user)

        return users

    def create_borrow_records(self, users, books):
        """Create 75 borrow records with various statuses"""
        records = []
        
        # Ensure we have enough books and users
        if not books or not users:
            self.stdout.write(self.style.WARNING('Not enough books or users to create borrow records'))
            return records
        
        for _ in range(75):
            user = random.choice(users)
            book = random.choice(books)
            
            # Random borrow date in the past 90 days
            days_ago = random.randint(1, 90)
            borrow_date = timezone.now() - timedelta(days=days_ago)
            
            # Due date is 14 days after borrow date
            due_date = borrow_date + timedelta(days=14)
            
            # Determine status and return date
            status_roll = random.random()
            if status_roll < 0.5:  # 50% returned
                status = 'returned'
                return_date = borrow_date + timedelta(days=random.randint(1, 14))
            elif status_roll < 0.8:  # 30% borrowed (on time)
                status = 'borrowed'
                return_date = None
            else:  # 20% overdue
                status = 'overdue'
                return_date = None
                due_date = timezone.now() - timedelta(days=random.randint(1, 30))
            
            # Create borrow record
            record = BorrowRecord.objects.create(
                user=user,
                book=book,
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date,
                status=status,
                notes=random.choice([
                    '',
                    'Excellent condition',
                    'Minor wear on cover',
                    'Requested renewal',
                    'First time borrower',
                    'Regular patron',
                ])
            )
            
            records.append(record)

        return records
