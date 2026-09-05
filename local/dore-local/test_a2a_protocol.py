import unittest
import a2a_protocol as p
from a2a_capabilities import Registry,CapabilityError

class ProtocolTests(unittest.TestCase):
 def test_round_trip_shape(self):
  q=p.request('dore.health',{'verbose':False},'1');self.assertEqual(p.validate(q),q)
 def test_rejects_unknown_fields(self):
  q=p.request('dore.health');q['command']='anything'
  with self.assertRaises(ValueError):p.validate(q)
 def test_registry_rejects_unknown_capability(self):
  r=Registry()
  with self.assertRaises(CapabilityError):r.invoke('shell.exec',{})
 def test_registered_capability(self):
  r=Registry();r.register('dore.health',lambda _: {'ok':True});self.assertEqual(r.invoke('dore.health'),{'ok':True})
 def test_describe_marks_availability(self):
  r=Registry();r.register('dore.health',lambda _: {'ok':True});rows={x['name']:x for x in r.describe()};self.assertTrue(rows['dore.health']['available']);self.assertFalse(rows['resident.update']['available'])

if __name__=='__main__':unittest.main()
