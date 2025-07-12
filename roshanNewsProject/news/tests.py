from tkinter.font import names

from django.test import TestCase
from .models import Tag, News
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.
class NewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.tag_tech = Tag.objects.create(name="تکنولوژی")
        self.tag_economy = Tag.objects.create(name="اقتصاد")
        self.tag_science = Tag.objects.create(name="علم")
        self.tag_interNational = Tag.objects.create(name="بین‌الملل")

        self.news1 = News.objects.create(title="تأثیرات فناوری اطلاعات بر بازار کار",
                                         content_news="فناوری اطلاعات باعث ایجاد تغییرات چشمگیری در بازار کار شده است. بسیاری از مشاغل جدید به دلیل این پیشرفت‌ها ایجاد شده‌اند...",
                                         reference="www.workforce.com")
        self.news1.tags.set([self.tag_tech, self.tag_economy])

        self.news2 = News.objects.create(title='پیشرفت‌های جدید در فناوری اطلاعات',
                                         content_news='فناوری اطلاعات به سرعت در حال پیشرفت است و تاثیرات زیادی بر زندگی روزمره مردم دارد...',
                                         reference="www.technews.com")
        self.news2.tags.set([self.tag_tech, self.tag_science])

        self.news3 = News.objects.create(title='تغییرات بزرگ در اقتصاد جهانی',
                                         content_news='اقتصاد جهان با چالش‌های بزرگ در سال 2025 روبه‌رو خواهد شد...',
                                         reference='www.globaleconomy.com')
        self.news3.tags.set([self.tag_economy, self.tag_interNational])


    def test_insert_test(self):
        data_news = {
            "title": "پیشرفت‌های جدید در علم داده",
            "content_news": "علم داده به سرعت در حال پیشرفت است و تاثیرات زیادی بر صنایع دارد...",
            "tags": [
                "علم"
            ],
            "reference": "www.datascience.com"
        }

        response = self.client.post("/api/news/insert/", data_news, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_news(self):
        response = self.client.get('/api/news/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'تأثیرات فناوری اطلاعات بر بازار کار')
        self.assertEqual(response.data[1]['title'], 'پیشرفت‌های جدید در فناوری اطلاعات')
        self.assertEqual(response.data[2]['title'], 'تغییرات بزرگ در اقتصاد جهانی')

    def test_tag_filter(self):
        response = self.client.get('/api/news/?tags=اقتصاد')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'تأثیرات فناوری اطلاعات بر بازار کار')
        self.assertEqual(response.data[1]['title'], 'تغییرات بزرگ در اقتصاد جهانی')

    def test_keyword_filter(self):
        response = self.client.get('/api/news/?keyword=فناوری اطلاعات')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'تأثیرات فناوری اطلاعات بر بازار کار')
        self.assertEqual(response.data[1]['title'], 'پیشرفت‌های جدید در فناوری اطلاعات')

    def test_exclude_keyword_filter(self):
        response = self.client.get('/api/news/?exclude_keyword=فناوری اطلاعات')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'تغییرات بزرگ در اقتصاد جهانی')

    def test_exclude_and_keyword(self):
        response = self.client.get('/api/news/?keyword=فناوری اطلاعات&exclude_keyword=مشاغل')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'پیشرفت‌های جدید در فناوری اطلاعات')
