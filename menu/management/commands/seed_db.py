# Eta React course er jonno dummy data AI diye baniyechi. Romjan Bhai bolse React er jonno AI allowed. Shudhu dummy data er jonno AI use korsi, bakigula 100% nije korsi.


# menu/management/commands/seed_db.py
import os
import requests
from django.core.management.base import BaseCommand
from menu.models import Category, FoodItem
from django.core.files.base import ContentFile
from faker import Faker
import random
import time

class Command(BaseCommand):
    help = 'Seeds the database with extensive dummy Bangladeshi restaurant data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        FoodItem.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        fake = Faker('en_BD')

        # --- Categories ---
        bangladeshi_categories = [
            "Starter", "Traditional Curries", "Biryani & Pulao",
            "Sea Food Delights", "Vegetarian Specials", "Street Food Favorites",
            "Grills & Kebabs", "Breads & Sides", "Desserts & Sweets", "Beverages"
        ]

        self.stdout.write(self.style.MIGRATE_HEADING('Creating categories...'))
        category_objects = {}
        for name in bangladeshi_categories:
            cat = Category.objects.create(name=name) 
            category_objects[name] = cat
            self.stdout.write(f'  - Created Category: {name}')
        self.stdout.write(self.style.SUCCESS('Categories seeded successfully.'))
        self.stdout.write('---')

        # --- Food Items with Real Descriptions ---
        self.stdout.write(self.style.MIGRATE_HEADING('Creating food items...'))
        food_details = {
            "Starter": [
                ("Vegetable Samosa", 80, "Crisp, triangular pastries filled with spiced potatoes and peas."),
                ("Chicken Lollipops", 180, "Juicy chicken wings shaped into lollipops, marinated and fried to perfection."),
                ("Prawn Tempura", 250, "Lightly battered and deep-fried prawns, served with a sweet chili sauce."),
                ("Dal Puri", 40, "A deep-fried flatbread stuffed with a flavorful lentil mixture."),
                ("Fish Cutlet", 120, "Spiced fish patties coated in breadcrumbs and fried until golden."),
                ("Beguni", 30, "Slices of eggplant coated in a spiced chickpea flour batter and fried."),
                ("Chotpoti", 150, "A classic street food featuring chickpeas and potatoes, topped with eggs and a tangy sauce."),
            ],
            "Traditional Curries": [
                ("Chicken Bhuna", 320, "A semi-dry chicken curry with rich, deep flavors from slow cooking."),
                ("Beef Kala Bhuna", 450, "A dark and spicy beef curry, a specialty of Chittagong with a unique aroma."),
                ("Mutton Rogan Josh", 480, "Tender mutton slow-cooked in a yogurt-based gravy with aromatic spices."),
                ("Prawn Malai Curry", 400, "Succulent prawns simmered in a creamy coconut milk-based curry."),
                ("Korma (Chicken/Beef)", 350, "A mild and creamy curry prepared with yogurt, nuts, and delicate spices."),
                ("Haleem", 280, "A hearty stew of lentils, wheat, and meat, slow-cooked for hours."),
                ("Chicken Rezala", 380, "A mild, elegant chicken curry known for its rich gravy and subtle flavors."),
                ("Duck Bhuna", 420, "A rich and spicy curry featuring tender duck meat, popular in rural Bangladesh."),
            ],
            "Biryani & Pulao": [
                ("Chicken Biryani", 300, "A fragrant rice dish with marinated chicken, layered and cooked to perfection."),
                ("Beef Tehari", 350, "Spicy and tender beef cooked with fine rice, a Dhaka city favorite."),
                ("Kacchi Biryani", 500, "Layers of fragrant basmati rice and tender marinated mutton, a royal delicacy."),
                ("Morog Polao", 380, "A classic celebration dish with fragrant rice and a whole chicken piece."),
                ("Mutton Biryani", 480, "Rich and flavorful mutton biryani with long-grain basmati rice and aromatic spices."),
                ("Vegetable Pulao", 220, "A light and flavorful rice pilaf with assorted fresh vegetables."),
            ],
            "Sea Food Delights": [
                ("Hilsha Fry", 600, "Crispy fried Hilsha fish, a national delicacy, seasoned with turmeric and chili."),
                ("Prawn Dopeyaza", 420, "Prawns cooked in a two-onion-based curry, rich in flavor."),
                ("Loitta Shutki Bhorta", 180, "A fiery fish mash made from dried Bombay duck, a rustic Bengali dish."),
                ("Chingri Malaikari", 550, "Jumbo prawns cooked in a creamy coconut gravy, a true Bengali comfort food."),
                ("Rui Fish Curry", 280, "A flavorful curry with slices of fresh rohu fish, cooked in a light gravy."),
                ("Pomfret Fry", 450, "Whole pomfret fish marinated with spices and fried until crispy."),
            ],
            "Vegetarian Specials": [
                ("Alu Bhorta", 70, "A simple yet delicious mash of spiced potatoes."),
                ("Begun Bhorta", 80, "Mashed eggplant mixed with herbs, onions, and mustard oil."),
                ("Dal Makhani", 180, "Creamy black lentils and kidney beans slow-cooked with butter and spices."),
                ("Mixed Vegetable Sabzi", 200, "A vibrant medley of fresh seasonal vegetables stir-fried with spices."),
                ("Paneer Butter Masala", 300, "Soft cubes of paneer simmered in a rich, creamy tomato gravy."),
                ("Shak Bhaji", 90, "Stir-fried leafy greens, a healthy and popular side dish."),
            ],
            "Street Food Favorites": [
                ("Fuchka", 120, "Hollow, crispy balls filled with spiced mashed potatoes and tamarind water."),
                ("Bhel Puri", 100, "A crunchy and tangy snack made with puffed rice, vegetables, and chutneys."),
                ("Doi Fuchka", 180, "Fuchka served with a creamy and sweet yogurt filling."),
                ("Singara Chaat", 140, "Crushed samosas topped with chickpeas, yogurt, and a variety of chutneys."),
                ("Chicken Shwarma", 220, "Marinated chicken cooked on a vertical rotisserie, served in a roll."),
                ("Egg Chop", 50, "A boiled egg wrapped in a spicy potato mixture and deep-fried."),
            ],
            "Grills & Kebabs": [
                ("Chicken Tikka", 280, "Tender chicken pieces marinated in yogurt and spices, grilled to perfection."),
                ("Beef Seekh Kebab", 350, "Spiced minced beef skewered and grilled until tender and juicy."),
                ("Boti Kebab", 320, "Small chunks of mutton marinated and grilled on skewers."),
                ("Tandoori Chicken", 400, "Chicken marinated in a yogurt and spice blend, roasted in a clay oven."),
                ("Grilled Prawns", 450, "Skewered prawns seasoned and grilled for a smoky flavor."),
                ("Paneer Tikka", 280, "Cubes of paneer and vegetables marinated and grilled, a vegetarian delight."),
            ],
            "Breads & Sides": [
                ("Plain Naan", 60, "Soft, pillowy flatbread baked in a tandoor oven."),
                ("Garlic Naan", 80, "Naan bread infused with fresh garlic and coriander."),
                ("Butter Naan", 70, "A flaky, soft naan brushed with clarified butter."),
                ("Paratha", 50, "A layered flatbread made with whole wheat flour."),
                ("Roti", 40, "Simple, unleavened whole wheat flatbread."),
                ("Basmati Rice", 100, "Fragrant, long-grain basmati rice, perfect with any curry."),
                ("Cucumber Raita", 90, "A cooling side dish of yogurt mixed with grated cucumber and spices."),
            ],
            "Desserts & Sweets": [
                ("Roshogolla", 60, "Spongy cottage cheese balls soaked in a light sugar syrup."),
                ("Mishti Doi", 120, "Sweet, caramelized yogurt, a Bengali classic."),
                ("Gulab Jamun", 70, "Soft, deep-fried milk dumplings soaked in a rose-scented syrup."),
                ("Shahi Tukra", 150, "Fried bread slices soaked in milk and topped with nuts."),
                ("Firni", 100, "A creamy rice pudding flavored with cardamom and rose water."),
                ("Kulfi", 80, "A rich, dense Indian ice cream, traditionally made in molds."),
                ("Gajer Halwa", 130, "A delicious dessert made from grated carrots, milk, and sugar."),
            ],
            "Beverages": [
                ("Borhani", 100, "A spicy, yogurt-based drink, often served with biryani."),
                ("Sweet Lassi", 120, "A creamy, yogurt-based smoothie with sugar."),
                ("Salted Lassi", 120, "A refreshing and savory yogurt drink with a hint of salt."),
                ("Fresh Lime Soda", 80, "A fizzy and tangy drink made with fresh lime juice."),
                ("Masala Tea", 70, "Spiced black tea brewed with a blend of aromatic herbs."),
                ("Cold Coffee", 150, "A chilled and frothy coffee drink, perfect for hot weather."),
                ("Mango Juice", 90, "Sweet and refreshing juice made from ripe mangoes."),
            ],
        }

        image_keywords = [
            "bangladeshi-food", "biryani", "curry", "dessert", "street-food",
            "kebab", "seafood", "breakfast", "drink", "traditional-meal"
        ]

        created_food_count = 0
        for cat_name, food_list in food_details.items():
            category = category_objects[cat_name]
            for name, base_price, description in food_list: # Now we are also iterating over 'description'
                is_special = random.choices([True, False], weights=[0.2, 0.8], k=1)[0]
                discount_price = None
                if is_special:
                    discount_price = round(base_price * random.uniform(0.7, 0.9), 2)

                keyword = random.choice(image_keywords)
                image_url = f"https://source.unsplash.com/random/800x600/?{keyword}"
                image_content = None

                try:
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    image_content = ContentFile(response.content, name=f'{name.replace(" ", "-").lower()}_{fake.uuid4()[:8]}.jpg')
                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f'  - Could not download image for {name} ({image_url}): {e}'))

                FoodItem.objects.create(
                    name=name,
                    description=description, # Using the pre-written description
                    price=base_price,
                    is_special=is_special,
                    discount_price=discount_price,
                    image=image_content,
                    category=category,
                )
                created_food_count += 1
                self.stdout.write(f'  - Created Food: {name} (Category: {cat_name})')
                time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_food_count} food items.'))
        self.stdout.write('---')
        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))