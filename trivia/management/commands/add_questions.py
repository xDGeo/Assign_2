from django.core.management.base import BaseCommand
from trivia.models import Question

class Command(BaseCommand):
    help = 'Add questions about European capitals to the database'

    def handle(self, *args, **options):
        questions = [
            {"question_text": "What is the capital of Albania?", "answer": "Tirana"},
            {"question_text": "What is the capital of Andorra?", "answer": "Andorra la Vella"},
            {"question_text": "What is the capital of Austria?", "answer": "Vienna"},
            {"question_text": "What is the capital of Belarus?", "answer": "Minsk"},
            {"question_text": "What is the capital of Belgium?", "answer": "Brussels"},
            {"question_text": "What is the capital of Bosnia and Herzegovina?", "answer": "Sarajevo"},
            {"question_text": "What is the capital of Bulgaria?", "answer": "Sofia"},
            {"question_text": "What is the capital of Croatia?", "answer": "Zagreb"},
            {"question_text": "What is the capital of Cyprus?", "answer": "Nicosia"},
            {"question_text": "What is the capital of Czech Republic?", "answer": "Prague"},
            {"question_text": "What is the capital of Denmark?", "answer": "Copenhagen"},
            {"question_text": "What is the capital of Estonia?", "answer": "Tallinn"},
            {"question_text": "What is the capital of Finland?", "answer": "Helsinki"},
            {"question_text": "What is the capital of France?", "answer": "Paris"},
            {"question_text": "What is the capital of Germany?", "answer": "Berlin"},
            {"question_text": "What is the capital of Greece?", "answer": "Athens"},
            {"question_text": "What is the capital of Hungary?", "answer": "Budapest"},
            {"question_text": "What is the capital of Iceland?", "answer": "Reykjavik"},
            {"question_text": "What is the capital of Ireland?", "answer": "Dublin"},
            {"question_text": "What is the capital of Italy?", "answer": "Rome"},
            {"question_text": "What is the capital of Kosovo?", "answer": "Pristina"},
            {"question_text": "What is the capital of Latvia?", "answer": "Riga"},
            {"question_text": "What is the capital of Liechtenstein?", "answer": "Vaduz"},
            {"question_text": "What is the capital of Lithuania?", "answer": "Vilnius"},
            {"question_text": "What is the capital of Luxembourg?", "answer": "Luxembourg"},
            {"question_text": "What is the capital of Malta?", "answer": "Valletta"},
            {"question_text": "What is the capital of Moldova?", "answer": "Chisinau"},
            {"question_text": "What is the capital of Monaco?", "answer": "Monaco"},
            {"question_text": "What is the capital of Montenegro?", "answer": "Podgorica"},
            {"question_text": "What is the capital of Netherlands?", "answer": "Amsterdam"},
            {"question_text": "What is the capital of North Macedonia?", "answer": "Skopje"},
            {"question_text": "What is the capital of Norway?", "answer": "Oslo"},
            {"question_text": "What is the capital of Poland?", "answer": "Warsaw"},
            {"question_text": "What is the capital of Portugal?", "answer": "Lisbon"},
            {"question_text": "What is the capital of Romania?", "answer": "Bucharest"},
            {"question_text": "What is the capital of Russia?", "answer": "Moscow"},
            {"question_text": "What is the capital of San Marino?", "answer": "San Marino"},
            {"question_text": "What is the capital of Serbia?", "answer": "Belgrade"},
            {"question_text": "What is the capital of Slovakia?", "answer": "Bratislava"},
            {"question_text": "What is the capital of Slovenia?", "answer": "Ljubljana"},
            {"question_text": "What is the capital of Spain?", "answer": "Madrid"},
            {"question_text": "What is the capital of Sweden?", "answer": "Stockholm"},
            {"question_text": "What is the capital of Switzerland?", "answer": "Bern"},
            {"question_text": "What is the capital of Ukraine?", "answer": "Kyiv"},
            {"question_text": "What is the capital of United Kingdom?", "answer": "London"},
            {"question_text": "What is the capital of Vatican City?", "answer": "Vatican City"},
        ]

        for question in questions:
            Question.objects.create(**question)

        self.stdout.write(self.style.SUCCESS('Successfully added questions'))
