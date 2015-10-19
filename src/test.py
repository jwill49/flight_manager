import io
from random import randint, choice
from ReservationSystem import ReservationSystem

def gen_transaction(name, rs):
  r = randint(0,2)
  
  if r == 0:
    route = choice(rs.route_manifest.keys())
    return ",".join(("BookPassenger",name, route))
  elif r == 1:
    route = choice(rs.route_manifest.keys())
    return ",".join(("CancelPassenger",name, route))
  else:
    flightno = choice(rs.flightno_manifest.keys())
    return ",".join(("ChangePrice",flightno, str(randint(50,1000))))
    

if __name__ == '__main__':
  names = []
  rs = ReservationSystem()
  rs.process_flight_manifest("in/inputfile1.txt")
  
  with io.open("in/names.txt", "rtU") as f:
    for n in f:
      names.append(n.strip())
  
  with io.open("in/inputfile3.txt", "wb") as f:
    for n in names:
      print >> f, gen_transaction(n, rs)
      
  rs.process_transactions("in/inputfile3.txt")
  rs.output_to_txt("out/test.txt")