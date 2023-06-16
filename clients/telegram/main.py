from models import *
from serializers import *
from managers import *

aobj1 = AbandonedObjectAPIManager.create(name='test', description='kuku epta', state='a', category='Bunker entrance')

print(aobj1.name)
print(aobj1.description)
print(AbandonedObjectSerializer.serialize(aobj1))
