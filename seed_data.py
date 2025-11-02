"""
Seed data script for populating the database with sample data
Run this script after setting up the database: python seed_data.py
"""

from app import create_app, db
from app.models import User, Category, Content, Comment, Subscription, Wishlist, ContentReview
from datetime import datetime, timedelta

def clear_data():
    """Clear all data from database"""
    print("Clearing existing data...")
    ContentReview.query.delete()
    Wishlist.query.delete()
    Subscription.query.delete()
    Comment.query.delete()
    Content.query.delete()
    Category.query.delete()
    User.query.delete()
    db.session.commit()
    print("Data cleared!")

def create_users():
    """Create sample users"""
    print("Creating users...")
    
    users = [
        User(
            username='admin',
            email='admin@moringa.com',
            password='Admin@123',
            role='admin',
            profile_data={'bio': 'System Administrator'}
        ),
        User(
            username='tech_writer1',
            email='writer1@moringa.com',
            password='Writer@123',
            role='tech_writer',
            profile_data={
                'bio': 'Senior Tech Writer specializing in DevOps',
                'expertise': ['DevOps', 'Cloud Computing', 'CI/CD']
            }
        ),
        User(
            username='tech_writer2',
            email='writer2@moringa.com',
            password='Writer@123',
            role='tech_writer',
            profile_data={
                'bio': 'Frontend Developer & Writer',
                'expertise': ['React', 'Vue.js', 'JavaScript']
            }
        ),
        User(
            username='john_doe',
            email='john@example.com',
            password='User@123',
            role='user',
            profile_data={
                'bio': 'Aspiring full-stack developer',
                'interests': ['Python', 'React', 'DevOps']
            }
        ),
        User(
            username='jane_smith',
            email='jane@example.com',
            password='User@123',
            role='user',
            profile_data={
                'bio': 'Data Science enthusiast',
                'interests': ['Python', 'Machine Learning', 'Data Analysis']
            }
        ),
        User(
            username='alex_dev',
            email='alex@example.com',
            password='User@123',
            role='user',
            profile_data={
                'bio': 'Mobile app developer',
                'interests': ['Flutter', 'React Native', 'Mobile Dev']
            }
        )
    ]
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    print(f"Created {len(users)} users!")
    return users

def create_categories(admin):
    """Create sample categories"""
    print("Creating categories...")
    
    categories = [
        Category(
            name='DevOps',
            description='DevOps practices, CI/CD, automation, and infrastructure',
            created_by=admin.id,
            slug='devops'
        ),
        Category(
            name='Frontend Development',
            description='HTML, CSS, JavaScript, React, Vue, Angular and frontend frameworks',
            created_by=admin.id,
            slug='frontend-development'
        ),
        Category(
            name='Backend Development',
            description='Server-side programming, APIs, databases, and backend frameworks',
            created_by=admin.id,
            slug='backend-development'
        ),
        Category(
            name='Full Stack',
            description='Full stack development covering both frontend and backend',
            created_by=admin.id,
            slug='full-stack'
        ),
        Category(
            name='Mobile Development',
            description='iOS, Android, Flutter, React Native and mobile app development',
            created_by=admin.id,
            slug='mobile-development'
        ),
        Category(
            name='Data Science',
            description='Data analysis, machine learning, AI, and data visualization',
            created_by=admin.id,
            slug='data-science'
        ),
        Category(
            name='Cloud Computing',
            description='AWS, Azure, GCP, cloud architecture and services',
            created_by=admin.id,
            slug='cloud-computing'
        ),
        Category(
            name='Career Advice',
            description='Tech career guidance, interview tips, and professional development',
            created_by=admin.id,
            slug='career-advice'
        )
    ]
    
    for category in categories:
        db.session.add(category)
    
    db.session.commit()
    print(f"Created {len(categories)} categories!")
    return categories

def create_content(users, categories):
    """Create sample content"""
    print("Creating content...")
    
    # Get specific users
    writer1 = next(u for u in users if u.username == 'tech_writer1')
    writer2 = next(u for u in users if u.username == 'tech_writer2')
    john = next(u for u in users if u.username == 'john_doe')
    
    # Get specific categories
    devops = next(c for c in categories if c.name == 'DevOps')
    frontend = next(c for c in categories if c.name == 'Frontend Development')
    backend = next(c for c in categories if c.name == 'Backend Development')
    career = next(c for c in categories if c.name == 'Career Advice')
    
    contents = [
        Content(
            title='Getting Started with Docker: A Complete Guide',
            content_type='article',
            author_id=writer1.id,
            category_id=devops.id,
            description='Learn Docker from scratch with practical examples and best practices',
            body='''Docker has revolutionized how we develop and deploy applications. In this comprehensive guide, we'll cover everything you need to know to get started with Docker.

## What is Docker?

Docker is a platform that enables developers to package applications into containers—standardized executable components combining application source code with the operating system libraries and dependencies required to run that code in any environment.

## Why Use Docker?

1. **Consistency**: Docker ensures your application runs the same way in development, testing, and production
2. **Isolation**: Each container is isolated from others, preventing conflicts
3. **Efficiency**: Containers share the host OS kernel, making them lightweight and fast
4. **Portability**: Run your containers anywhere Docker is installed

## Getting Started

First, install Docker from docker.com. Then, let's run your first container:

```bash
docker run hello-world
```

This simple command will download and run a test container. Let's break down what happened...''',
            thumbnail_url='https://picsum.photos/seed/docker/800/400',
            status='approved',
            views_count=245,
            likes_count=89,
            dislikes_count=3
        ),
        Content(
            title='React Hooks: Complete Tutorial',
            content_type='video',
            author_id=writer2.id,
            category_id=frontend.id,
            description='Master React Hooks with practical examples and real-world use cases',
            content_url='https://www.youtube.com/watch?v=example',
            thumbnail_url='https://picsum.photos/seed/react/800/400',
            status='approved',
            views_count=532,
            likes_count=156,
            dislikes_count=8
        ),
        Content(
            title='Building RESTful APIs with Flask',
            content_type='article',
            author_id=writer1.id,
            category_id=backend.id,
            description='Learn how to build robust RESTful APIs using Flask and Python',
            body='Flask is a lightweight Python web framework that makes it easy to build RESTful APIs...',
            thumbnail_url='https://picsum.photos/seed/flask/800/400',
            status='approved',
            views_count=187,
            likes_count=67,
            dislikes_count=4
        ),
        Content(
            title='Interview with Moringa Alumni: Sarah\'s Journey to Google',
            content_type='audio',
            author_id=writer2.id,
            category_id=career.id,
            description='Sarah shares her journey from Moringa School to becoming a software engineer at Google',
            content_url='https://example.com/audio/sarah-interview.mp3',
            thumbnail_url='https://picsum.photos/seed/interview/800/400',
            status='approved',
            views_count=412,
            likes_count=198,
            dislikes_count=2
        ),
        Content(
            title='CI/CD Pipeline with GitHub Actions',
            content_type='article',
            author_id=writer1.id,
            category_id=devops.id,
            description='Automate your deployment workflow with GitHub Actions',
            body='Continuous Integration and Continuous Deployment are essential practices in modern software development...',
            thumbnail_url='https://picsum.photos/seed/cicd/800/400',
            status='approved',
            views_count=321,
            likes_count=112,
            dislikes_count=6
        ),
        Content(
            title='CSS Grid vs Flexbox: When to Use Each',
            content_type='video',
            author_id=writer2.id,
            category_id=frontend.id,
            description='Understanding the differences and use cases for CSS Grid and Flexbox',
            content_url='https://www.youtube.com/watch?v=example2',
            thumbnail_url='https://picsum.photos/seed/css/800/400',
            status='approved',
            views_count=289,
            likes_count=94,
            dislikes_count=3
        ),
        Content(
            title='My First Web App Project',
            content_type='article',
            author_id=john.id,
            category_id=frontend.id,
            description='A beginner shares their experience building their first web application',
            body='As a Moringa School student, I just completed my first web application...',
            thumbnail_url='https://picsum.photos/seed/project/800/400',
            status='pending',
            views_count=0,
            likes_count=0,
            dislikes_count=0
        ),
        Content(
            title='10 Tips for Technical Interviews',
            content_type='article',
            author_id=writer2.id,
            category_id=career.id,
            description='Essential tips to ace your next technical interview',
            body='Technical interviews can be challenging, but with proper preparation, you can succeed...',
            thumbnail_url='https://picsum.photos/seed/tips/800/400',
            status='approved',
            views_count=678,
            likes_count=234,
            dislikes_count=12
        )
    ]
    
    # Set published dates for approved content
    base_date = datetime.utcnow() - timedelta(days=30)
    for i, content in enumerate(contents):
        if content.status == 'approved':
            content.published_at = base_date + timedelta(days=i * 3)
        db.session.add(content)
    
    db.session.commit()
    print(f"Created {len(contents)} content items!")
    return contents

def create_comments(users, contents):
    """Create sample comments"""
    print("Creating comments...")
    
    john = next(u for u in users if u.username == 'john_doe')
    jane = next(u for u in users if u.username == 'jane_smith')
    alex = next(u for u in users if u.username == 'alex_dev')
    
    # Get first content item
    docker_article = contents[0]
    
    comments = [
        Comment(
            comment_text='This is exactly what I needed! Clear and concise explanation.',
            content_id=docker_article.id,
            user_id=john.id
        ),
        Comment(
            comment_text='Great tutorial! Could you cover Docker Compose next?',
            content_id=docker_article.id,
            user_id=jane.id
        ),
        Comment(
            comment_text='Very helpful for beginners like me. Thanks!',
            content_id=docker_article.id,
            user_id=alex.id
        )
    ]
    
    for comment in comments:
        db.session.add(comment)
    
    db.session.commit()
    
    # Create a reply to first comment
    parent_comment = comments[0]
    reply = Comment(
        comment_text='Glad it helped! Feel free to ask if you have any questions.',
        content_id=docker_article.id,
        user_id=users[1].id,  # writer1
        parent_comment_id=parent_comment.id
    )
    db.session.add(reply)
    db.session.commit()
    
    print(f"Created {len(comments) + 1} comments (including replies)!")
    return comments

def create_subscriptions(users, categories):
    """Create sample subscriptions"""
    print("Creating subscriptions...")
    
    john = next(u for u in users if u.username == 'john_doe')
    jane = next(u for u in users if u.username == 'jane_smith')
    
    devops = next(c for c in categories if c.name == 'DevOps')
    frontend = next(c for c in categories if c.name == 'Frontend Development')
    data_science = next(c for c in categories if c.name == 'Data Science')
    
    subscriptions = [
        Subscription(user_id=john.id, category_id=devops.id),
        Subscription(user_id=john.id, category_id=frontend.id),
        Subscription(user_id=jane.id, category_id=data_science.id),
        Subscription(user_id=jane.id, category_id=frontend.id)
    ]
    
    for sub in subscriptions:
        db.session.add(sub)
    
    db.session.commit()
    print(f"Created {len(subscriptions)} subscriptions!")

def create_wishlists(users, contents):
    """Create sample wishlist items"""
    print("Creating wishlist items...")
    
    john = next(u for u in users if u.username == 'john_doe')
    jane = next(u for u in users if u.username == 'jane_smith')
    
    wishlists = [
        Wishlist(user_id=john.id, content_id=contents[1].id),
        Wishlist(user_id=john.id, content_id=contents[4].id),
        Wishlist(user_id=jane.id, content_id=contents[0].id),
        Wishlist(user_id=jane.id, content_id=contents[3].id)
    ]
    
    for wishlist in wishlists:
        db.session.add(wishlist)
    
    db.session.commit()
    print(f"Created {len(wishlists)} wishlist items!")

def create_reviews(users, contents):
    """Create sample content reviews"""
    print("Creating content reviews...")
    
    john = next(u for u in users if u.username == 'john_doe')
    jane = next(u for u in users if u.username == 'jane_smith')
    alex = next(u for u in users if u.username == 'alex_dev')
    
    reviews = [
        ContentReview(content_id=contents[0].id, user_id=john.id, review_type='like'),
        ContentReview(content_id=contents[1].id, user_id=john.id, review_type='like'),
        ContentReview(content_id=contents[0].id, user_id=jane.id, review_type='like'),
        ContentReview(content_id=contents[3].id, user_id=jane.id, review_type='like'),
        ContentReview(content_id=contents[1].id, user_id=alex.id, review_type='like'),
        ContentReview(content_id=contents[2].id, user_id=alex.id, review_type='dislike')
    ]
    
    for review in reviews:
        db.session.add(review)
    
    db.session.commit()
    
    # Update content counts
    for content in contents:
        ContentReview.update_content_counts(content.id)
    
    print(f"Created {len(reviews)} reviews!")

def seed_database():
    """Main function to seed the database"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*50)
        print("Starting database seeding...")
        print("="*50 + "\n")
        
        # Clear existing data
        clear_data()
        
        # Create all data
        users = create_users()
        categories = create_categories(users[0])  # admin is first user
        contents = create_content(users, categories)
        comments = create_comments(users, contents)
        create_subscriptions(users, categories)
        create_wishlists(users, contents)
        create_reviews(users, contents)
        
        print("\n" + "="*50)
        print("Database seeding completed successfully!")
        print("="*50)
        print("\nTest Accounts Created:")
        print("-" * 50)
        print("Admin:")
        print("  Email: admin@moringa.com")
        print("  Password: Admin@123")
        print("\nTech Writers:")
        print("  Email: writer1@moringa.com")
        print("  Password: Writer@123")
        print("  Email: writer2@moringa.com")
        print("  Password: Writer@123")
        print("\nUsers:")
        print("  Email: john@gmail.com")
        print("  Password: User@123")
        print("  Email: jane@gmail.com")
        print("  Password: User@123")
        print("  Email: alex@gmail.com")
        print("  Password: User@123")
        print("-" * 50)

if __name__ == '__main__':
    seed_database()