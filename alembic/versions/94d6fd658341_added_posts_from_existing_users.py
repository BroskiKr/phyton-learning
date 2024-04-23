"""added posts from existing users

Revision ID: 94d6fd658341
Revises: 14baae79cdc6
Create Date: 2024-04-22 19:34:14.666298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app import models

# revision identifiers, used by Alembic.
revision: str = '94d6fd658341'
down_revision: Union[str, None] = '14baae79cdc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(models.Post.__table__,[
    {
        "title": "How to Improve Concentration at Work",
        "body": "Practical tips and strategies for enhancing concentration and productivity while working.",
        "owner_id": 2
    },
    {
        "title": "Ideas for a Healthy Breakfast",
        "body": "Tasty and healthy breakfast ideas to start your day with energy and vitality.",
        "owner_id": 2
    },
    {
        "title": "Self-Development Techniques That Will Change Your Life",
        "body": "Learn about effective self-development techniques that will help you become a better version of yourself.",
        "owner_id": 3
    },
    {
        "title": "10 Places Worth Visiting in Your City",
        "body": "Discover the best places and attractions in your city for an unforgettable time.",
        "owner_id": 4
    },
    {
        "title": "Secrets of Effective Time Management",
        "body": "Learn to manage your time effectively and achieve more in a short period.",
        "owner_id": 4
    },
    {
        "title": "Recipes for Healthy Children's Breakfasts",
        "body": "Tasty and nutritious breakfast recipes that kids love and that will help them start the day right.",
        "owner_id": 4
    },
    {
        "title": "How to Overcome Stress at Work",
        "body": "Practical tips and strategies for effectively managing stress during the workday.",
        "owner_id": 2
    },
    {
        "title": "Training for Increased Energy and Endurance",
        "body": "Effective exercises and workouts to increase energy and endurance throughout the day.",
        "owner_id": 3
    },
    {
        "title": "5 Books for Summer Reading",
        "body": "A list of exciting books to read this summer to enjoy leisure and personal development.",
        "owner_id": 5
    },
    {
        "title": "How to Find a Balance Between Work and Personal Life",
        "body": "Tips and strategies for achieving harmony between career and personal life to maintain health and happiness.",
        "owner_id": 5
    },
    {
        "title": "The Art of Mindful Eating",
        "body": "Discover the benefits of mindful eating and learn how to cultivate a healthier relationship with food.",
        "owner_id": 2
    },
    {
        "title": "Mastering the Art of Public Speaking",
        "body": "Effective techniques and exercises to overcome stage fright and deliver powerful speeches with confidence.",
        "owner_id": 3
    },
    {
        "title": "Exploring Nature: Hiking Trails Near You",
        "body": "Uncover the beauty of nature with a guide to the best hiking trails in your area, perfect for outdoor enthusiasts.",
        "owner_id": 4
    },
    {
        "title": "The Power of Gratitude: Transform Your Life",
        "body": "Learn how practicing gratitude can positively impact your life and well-being.",
        "owner_id": 5
    },
    {
        "title": "Effective Communication Strategies for Couples",
        "body": "Tools and techniques to improve communication and strengthen relationships with your partner.",
        "owner_id": 2
    },
    {
        "title": "Unlocking Creativity: Tips for Artists and Writers",
        "body": "Explore methods to unleash your creative potential and overcome creative blocks in your artistic endeavors.",
        "owner_id": 3
    },
    {
        "title": "Budget-Friendly Travel Destinations",
        "body": "Discover affordable yet exciting travel destinations for your next adventure.",
        "owner_id": 4
    },
    {
        "title": "Mindfulness Meditation: A Beginner's Guide",
        "body": "Learn the basics of mindfulness meditation and its benefits for reducing stress and promoting overall well-being.",
        "owner_id": 5
    },
    {
        "title": "Effective Home Organization Tips",
        "body": "Practical advice and strategies for decluttering and organizing your living space for improved productivity and peace of mind.",
        "owner_id": 2
    },
    {
        "title": "The Science of Happiness: Strategies for a Fulfilling Life",
        "body": "Discover evidence-based approaches to cultivate happiness and enhance overall life satisfaction.",
        "owner_id": 3
    }
        ])


def downgrade() -> None:
    op.execute("DELETE FROM posts WHERE id > 0 AND id < 11")
