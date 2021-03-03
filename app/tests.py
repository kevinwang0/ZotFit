from django.test import TestCase
from .models import MemberManager, Member
from django.contrib.auth.models import User
import datetime

# Create your tests here.
class MemberHelperTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('Chevy Chase', 'chevy@chase.com', 'chevyspassword')
        Member.objects.createMember(User.objects.get(id=1), height = 80, weight = 180, birth = datetime.date(1998, 10, 19))

    def testAgeScore(self):
    	member = Member.objects.get(id=1)
    	print('Age Score: ' + str(member.ageScore()))
    	self.assertEqual(member.ageScore(), 11)

    def testBMIScore(self):
        member = Member.objects.get(id=1)
        print('BMI Score: ' + str(member.bmiScore()))
        self.assertEqual(member.bmiScore(), 9)

    def testHealthScore(self):
        member = Member.objects.get(id=1)
        print('Health Score: ' + str(member.healthScore()))
        self.assertEqual(member.healthScore(), 20)
