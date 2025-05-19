from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from unidecode import unidecode
import random
from products.models import Brand, Category, Product

class Command(BaseCommand):
    help = 'Inserts 1000 test products with brands and categories'

    def handle(self, *args, **kwargs):
        fake = Faker()

        BRANDS = [
            ("Nestlé", "نستله"),
            ("Almarai", "المراعي"),
            ("PepsiCo", "بيبسيكو"),
            ("Unilever", "يونيليفر"),
            ("Kraft Heinz", "كرافت هاينز"),
            ("Danone", "دانون"),
            ("Coca-Cola", "كوكاكولا"),
            ("Mondelēz", "مونديليز"),
            ("General Mills", "جنرال ميلز"),
            ("Mars", "مارس"),
            ("Procter & Gamble", "بروكتر آند جامبل"),
            ("Kellogg's", "كيلوجز"),
            ("Ferrero", "فيريرو"),
            ("Barilla", "باريلا"),
            ("Arla Foods", "أرلا فودز"),
            ("Lactalis", "لاكتاليس"),
            ("FrieslandCampina", "فريزلاند كامبينا"),
            ("Tropicana", "تروبيكانا"),
            ("Cadbury", "كادبوري"),
            ("Lipton", "ليبتون"),
        ]

        # Realistic Categories (English, Arabic)
        CATEGORIES = [
            ("Dairy", "منتجات الألبان"),
            ("Beverages", "المشروبات"),
            ("Snacks", "الوجبات الخفيفة"),
            ("Bakery", "المخبوزات"),
            ("Canned Goods", "المعلبات"),
            ("Frozen Foods", "الأطعمة المجمدة"),
            ("Meat & Poultry", "اللحوم والدواجن"),
            ("Seafood", "المأكولات البحرية"),
            ("Fruits & Vegetables", "الفواكه والخضروات"),
            ("Cereals & Grains", "الحبوب والمكرونة"),
        ]

        # Realistic Product Names (English, Arabic)
        PRODUCT_NAMES = [
            ("Chocolate Milk", "حليب بالشوكولاتة"),
            ("Strawberry Yogurt", "زبادي بالفراولة"),
            ("Orange Juice", "عصير برتقال"),
            ("Cola Drink", "مشروب كولا"),
            ("Potato Chips", "رقائق البطاطس"),
            ("Butter Croissant", "كرواسون بالزبدة"),
            ("Tuna Can", "تونة معلبة"),
            ("Frozen Pizza", "بيتزا مجمدة"),
            ("Chicken Breast", "صدر دجاج"),
            ("Salmon Fillet", "فيليه السلمون"),
            ("Apple", "تفاحة"),
            ("Carrot", "جزر"),
            ("Corn Flakes", "كورن فليكس"),
            ("Spaghetti", "سباغيتي"),
            ("Vanilla Ice Cream", "آيس كريم الفانيليا"),
            ("Cheddar Cheese", "جبنة شيدر"),
            ("Green Tea", "شاي أخضر"),
            ("Peanut Butter", "زبدة الفول السوداني"),
            ("Tomato Sauce", "صلصة طماطم"),
            ("Beef Sausage", "نقانق لحم البقر"),
            ("Shrimp", "جمبري"),
            ("Banana", "موز"),
            ("Broccoli", "بروكلي"),
            ("Oatmeal", "شوفان"),
            ("White Bread", "خبز أبيض"),
            ("Mango Juice", "عصير مانجو"),
            ("Salted Crackers", "بسكويت مملح"),
            ("Fruit Salad", "سلطة فواكه"),
            ("Grilled Chicken", "دجاج مشوي"),
            ("Sardines", "سردين"),
            ("Spinach", "سبانخ"),
            ("Rice Cereal", "حبوب الأرز"),
            ("Pasta Alfredo", "باستا ألفريدو"),
            ("Greek Yogurt", "زبادي يوناني"),
            ("Lemonade", "ليمونادا"),
            ("Cheese Puffs", "نفاش الجبن"),
            ("Whole Wheat Bread", "خبز القمح الكامل"),
            ("Corn Soup", "حساء الذرة"),
            ("Frozen Fries", "بطاطس مجمدة"),
            ("Turkey Slices", "شرائح ديك رومي"),
            ("Cod Fish", "سمك القد"),
            ("Grapes", "عنب"),
            ("Cucumber", "خيار"),
            ("Granola", "جرانولا"),
            ("Lasagna", "لازانيا"),
            ("Mozzarella Sticks", "أصابع الموزاريلا"),
            ("Iced Coffee", "قهوة مثلجة"),
            ("Popcorn", "فشار"),
            ("Olive Oil", "زيت زيتون"),
            ("Pork Bacon", "لحم خنزير مقدد"),
            ("Crab Sticks", "أصابع السلطعون"),
            ("Pineapple", "أناناس"),
            ("Tomato", "طماطم"),
            ("Wheat Bran", "نخالة القمح"),
            ("Macaroni", "مكرونة"),
            ("Blueberry Muffin", "مافن التوت"),
            ("Energy Drink", "مشروب طاقة"),
            ("Chocolate Bar", "لوح الشوكولاتة"),
            ("Canned Beans", "فاصوليا معلبة"),
            ("Frozen Berries", "توت مجمد"),
            ("Lamb Chops", "شرائح لحم الضأن"),
            ("Tuna Steak", "ستيك التونة"),
            ("Orange", "برتقال"),
            ("Lettuce", "خس"),
            ("Puffed Rice", "أرز منفوخ"),
            ("Ravioli", "رافيولي"),
            ("Cream Cheese", "جبنة كريمية"),
            ("Sparkling Water", "مياه فوارة"),
            ("Pretzels", "بريتزل"),
            ("Soy Sauce", "صلصة الصويا"),
            ("Beef Jerky", "لحم بقري مجفف"),
            ("Scallops", "إسكالوب"),
            ("Peach", "خوخ"),
            ("Zucchini", "كوسا"),
            ("Muesli", "ميوسلي"),
            ("Penne Pasta", "باستا بيني"),
            ("Donut", "دونات"),
            ("Apple Juice", "عصير تفاح"),
            ("Tortilla Chips", "رقائق التورتيلا"),
            ("Canned Peas", "بازلاء معلبة"),
            ("Frozen Vegetables", "خضروات مجمدة"),
            ("Pork Ribs", "ضلوع لحم الخنزير"),
            ("Mackerel", "ماكريل"),
            ("Strawberry", "فراولة"),
            ("Onion", "بصل"),
            ("Quinoa", "كينوا"),
            ("Fusilli Pasta", "باستا فوسيلي"),
            ("Bagel", "بيجل"),
            ("Ginger Ale", "جنجر إيل"),
            ("Trail Mix", "مزيج المكسرات"),
            ("Canned Corn", "ذرة معلبة"),
            ("Frozen Chicken Wings", "أجنحة دجاج مجمدة"),
            ("Duck Breast", "صدر البط"),
            ("Lobster", "الكركند"),
            ("Watermelon", "بطيخ"),
            ("Bell Pepper", "فلفل رومي"),
            ("Barley", "شعير"),
            ("Couscous", "كسكس"),
        ]

        @transaction.atomic
        def insert_test_data(self):
            # Clear existing data (optional, comment out to append)
            Product.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.all().delete()

            # Create Brands
            brand_objects = [Brand(name=name, name_ar=name_ar) for name, name_ar in BRANDS]
            Brand.objects.bulk_create(brand_objects)
            brands = list(Brand.objects.all())

            # Create Categories
            category_objects = [Category(name=name, name_ar=name_ar) for name, name_ar in CATEGORIES]
            Category.objects.bulk_create(category_objects)
            categories = list(Category.objects.all())

            # Create Products
            products = []
            for i in range(1000):
                # Cycle through PRODUCT_NAMES for variety
                name, name_ar = PRODUCT_NAMES[i % len(PRODUCT_NAMES)]
                # Add variation to avoid duplicates
                if i >= len(PRODUCT_NAMES):
                    name = f"{name} {fake.word().capitalize()}"
                    name_ar = f"{name_ar} {fake.word().capitalize()}"

                # Random nutrition facts
                nutrition_facts = {
                    "calories": random.randint(50, 600),
                    "fat": round(random.uniform(0, 40), 1),
                    "protein": round(random.uniform(0, 30), 1),
                    "carbohydrates": round(random.uniform(0, 80), 1),
                    "sugar": round(random.uniform(0, 50), 1)
                }

                products.append(Product(
                    name=name,
                    name_ar=name_ar,
                    brand=random.choice(brands),
                    category=random.choice(categories),
                    nutrition_facts=nutrition_facts
                ))

            # Bulk create products
            Product.objects.bulk_create(products)

            # Update search_vector for all products
            updated = 0
            for product in Product.objects.all():
                product.save()  # Triggers update_search_vector signal
                updated += 1
                if updated % 100 == 0:
                    print(f"Updated search_vector for {updated} products...")

            print(f"Inserted {Brand.objects.count()} brands, {Category.objects.count()} categories, "
                f"and {Product.objects.count()} products.")

        insert_test_data(self)
