#!/usr/bin/env python
"""
Script to load seed data from seed3.sql into Django models
This script parses the SQL INSERT statements and uses Django ORM to insert data
"""

import os
import sys
import django
import re
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from blog_app.models import PostStatus, Category, Tag, Post
from django.contrib.auth.models import User

def parse_sql_file(filename):
    """Parse the SQL file and extract INSERT statements"""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find all INSERT statements
    insert_pattern = r'INSERT INTO (\w+) \([^)]+\) VALUES\s*([^;]+);'
    matches = re.findall(insert_pattern, content, re.MULTILINE | re.DOTALL)
    
    data = {}
    for table, values_str in matches:
        if table not in data:
            data[table] = []
        
        # Parse individual value tuples - handle nested parentheses better
        values_str = values_str.strip()
        
        # Split by '),(' to get individual tuples
        if values_str.startswith('(') and values_str.endswith(')'):
            # Handle single tuple
            tuple_strings = [values_str]
        else:
            # Handle multiple tuples - split more carefully
            tuple_strings = []
            current_tuple = ''
            paren_count = 0
            in_quotes = False
            quote_char = None
            
            i = 0
            while i < len(values_str):
                char = values_str[i]
                
                if char in ["'", '"'] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char and in_quotes:
                    # Check if it's an escaped quote
                    if i + 1 < len(values_str) and values_str[i + 1] == quote_char:
                        current_tuple += char
                        i += 1  # Skip the next quote
                    else:
                        in_quotes = False
                        quote_char = None
                elif not in_quotes:
                    if char == '(':
                        paren_count += 1
                    elif char == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            current_tuple += char
                            tuple_strings.append(current_tuple.strip())
                            current_tuple = ''
                            # Skip comma and whitespace
                            while i + 1 < len(values_str) and values_str[i + 1] in ', \n\t':
                                i += 1
                            i += 1
                            continue
                
                current_tuple += char
                i += 1
            
            # Add any remaining tuple
            if current_tuple.strip():
                tuple_strings.append(current_tuple.strip())
        
        for tuple_str in tuple_strings:
            # Remove parentheses and split by comma, handling quoted strings
            tuple_str = tuple_str.strip('()')
            values = []
            current_value = ''
            in_quotes = False
            quote_char = None
            
            i = 0
            while i < len(tuple_str):
                char = tuple_str[i]
                if char in ["'", '"'] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char and in_quotes:
                    # Check if it's an escaped quote
                    if i + 1 < len(tuple_str) and tuple_str[i + 1] == quote_char:
                        current_value += char
                        i += 1  # Skip the next quote
                    else:
                        in_quotes = False
                        quote_char = None
                elif char == ',' and not in_quotes:
                    values.append(current_value.strip())
                    current_value = ''
                    i += 1
                    continue
                else:
                    current_value += char
                i += 1
            
            # Add the last value
            if current_value.strip():
                values.append(current_value.strip())
            
            data[table].append(values)
    
    return data

def clean_value(value):
    """Clean and convert SQL values to Python values"""
    value = value.strip()
    
    # Handle NULL
    if value.upper() == 'NULL':
        return None
    
    # Handle quoted strings
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1].replace("''", "'").replace('""', '"')
    
    # Handle numbers
    if value.isdigit():
        return int(value)
    
    # Handle boolean-like values
    if value in ['0', '1']:
        return bool(int(value))
    
    # Handle dates
    if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', value):
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    
    return value

def load_data():
    """Load data from seed3.sql into Django models"""
    print("Parsing seed3.sql...")
    data = parse_sql_file('seed3.sql')
    
    # Create a default user if none exists
    if not User.objects.exists():
        print("Creating default user...")
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
    else:
        user = User.objects.first()
    
    # Load PostStatus data
    if 'blog_app_poststatus' in data:
        print(f"Loading {len(data['blog_app_poststatus'])} PostStatus records...")
        PostStatus.objects.all().delete()  # Clear existing data
        
        for values in data['blog_app_poststatus']:
            cleaned_values = [clean_value(v) for v in values]
            PostStatus.objects.create(
                id=cleaned_values[0],
                name=cleaned_values[1],
                slug=cleaned_values[2],
                description=cleaned_values[3],
                icon=cleaned_values[4],
                color=cleaned_values[5],
                is_published=cleaned_values[6],
                is_active=cleaned_values[7],
                sort_order=cleaned_values[8],
                created_at=cleaned_values[9],
                updated_at=cleaned_values[10]
            )
    
    # Load Category data
    if 'blog_app_category' in data:
        print(f"Loading {len(data['blog_app_category'])} Category records...")
        Category.objects.all().delete()  # Clear existing data
        
        for values in data['blog_app_category']:
            cleaned_values = [clean_value(v) for v in values]
            Category.objects.create(
                id=cleaned_values[0],
                name=cleaned_values[1],
                slug=cleaned_values[2],
                description=cleaned_values[3],
                created_at=cleaned_values[4],
                updated_at=cleaned_values[5]
            )
    
    # Load Tag data
    if 'blog_app_tag' in data:
        print(f"Loading {len(data['blog_app_tag'])} Tag records...")
        Tag.objects.all().delete()  # Clear existing data
        
        for values in data['blog_app_tag']:
            cleaned_values = [clean_value(v) for v in values]
            Tag.objects.create(
                id=cleaned_values[0],
                name=cleaned_values[1],
                slug=cleaned_values[2],
                created_at=cleaned_values[3]
            )
    
    # Load Post data
    if 'blog_app_post' in data:
        print(f"Loading {len(data['blog_app_post'])} Post records...")
        Post.objects.all().delete()  # Clear existing data
        
        for values in data['blog_app_post']:
            cleaned_values = [clean_value(v) for v in values]
            
            # Debug: print the number of values
            print(f"Processing post with {len(cleaned_values)} values: {cleaned_values[:3]}...")
            
            # Ensure we have enough values
            if len(cleaned_values) < 13:
                print(f"Warning: Post record has only {len(cleaned_values)} values, skipping...")
                continue
            
            # Get related objects
            category = Category.objects.get(id=cleaned_values[6]) if cleaned_values[6] else None
            status = PostStatus.objects.get(id=cleaned_values[7]) if cleaned_values[7] else None
            
            post = Post.objects.create(
                id=cleaned_values[0],
                title=cleaned_values[1],
                slug=cleaned_values[2],
                author=user,  # Use the default user
                content=cleaned_values[4],
                excerpt=cleaned_values[5],
                category=category,
                status=status,
                featured_image=cleaned_values[8],
                meta_description=cleaned_values[9],
                created_at=cleaned_values[10],
                updated_at=cleaned_values[11],
                published_at=cleaned_values[12]
            )
    
    # Load Post-Tag relationships
    if 'blog_app_post_tags' in data:
        print(f"Loading {len(data['blog_app_post_tags'])} Post-Tag relationships...")
        
        for values in data['blog_app_post_tags']:
            cleaned_values = [clean_value(v) for v in values]
            post_id = cleaned_values[1]
            tag_id = cleaned_values[2]
            
            try:
                post = Post.objects.get(id=post_id)
                tag = Tag.objects.get(id=tag_id)
                post.tags.add(tag)
            except (Post.DoesNotExist, Tag.DoesNotExist):
                print(f"Warning: Could not find post {post_id} or tag {tag_id}")
    
    print("Data loading completed successfully!")

if __name__ == '__main__':
    load_data()