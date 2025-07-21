from django.core.management.base import BaseCommand
from api.models import Category, Tag

class Command(BaseCommand):
    help = 'Populate database with initial categories and tags'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing categories and tags before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing categories and tags...'))
            Category.objects.all().delete()
            Tag.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared successfully'))

        # Categories to create
        categories_data = [
            {'name': 'Technology', 'description': 'Posts about technology, programming, and software development'},
            {'name': 'Science', 'description': 'Scientific discoveries, research, and innovations'},
            {'name': 'Health', 'description': 'Health tips, medical news, and wellness advice'},
            {'name': 'Travel', 'description': 'Travel guides, destinations, and experiences'},
            {'name': 'Food', 'description': 'Recipes, restaurant reviews, and culinary adventures'},
            {'name': 'Lifestyle', 'description': 'Life tips, personal development, and lifestyle content'},
            {'name': 'Sports', 'description': 'Sports news, analysis, and commentary'},
            {'name': 'Entertainment', 'description': 'Movies, music, games, and entertainment news'},
            {'name': 'Business', 'description': 'Business news, entrepreneurship, and finance'},
            {'name': 'Education', 'description': 'Educational content, tutorials, and learning resources'},
        ]

        # Tags to create
        tags_data = [
            'python', 'django', 'javascript', 'web-development', 'mobile-app',
            'artificial-intelligence', 'machine-learning', 'data-science', 'blockchain',
            'cybersecurity', 'cloud-computing', 'devops', 'frontend', 'backend',
            'tutorial', 'beginners', 'advanced', 'tips-and-tricks', 'best-practices',
            'review', 'news', 'opinion', 'analysis', 'case-study',
            'productivity', 'career', 'remote-work', 'startup', 'innovation',
            'fitness', 'nutrition', 'mental-health', 'cooking', 'recipe',
            'adventure', 'budget-travel', 'photography', 'nature', 'culture',
            'movies', 'books', 'gaming', 'music', 'art',
            'finance', 'investment', 'marketing', 'management', 'leadership'
        ]

        # Create categories
        created_categories = 0
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                created_categories += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        # Create tags
        created_tags = 0
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_tags += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created tag: {tag.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Tag already exists: {tag.name}')
                )

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary:\n'
                f'Categories created: {created_categories}\n'
                f'Tags created: {created_tags}\n'
                f'Total categories in DB: {Category.objects.count()}\n'
                f'Total tags in DB: {Tag.objects.count()}'
            )
        )
