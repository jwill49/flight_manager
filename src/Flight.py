from collections import deque
from FlightPassenger import FlightPassenger
from sys import stderr
from shared import fmt

class Flight:
  def __init__(self, flightno, capacity, price, source, destination):
    self.flightno = flightno
    self.available_seats = deque(xrange(int(capacity)))
    self.price = float(price)
    self.source = source
    self.destination = destination
    self.route_key = source + "," + destination
    self.revenue = 0.0
    self.passenger_manifest = {} # Mapping from name ==> FlightPassenger
    
    print >> stderr, "Added flight", flightno, self.route_key, "$"+price, "with", capacity, "seats available."
    
  def __str__(self):
    return "Flight#: {0!s} Number of seats available: {1!s}\nTotal seats sold: {2!s}\nTotal revenue on this flight: ${3!s}\n\n{4!s}\n{5!s}\n".format(
      self.flightno, 
      len(self.available_seats), 
      len(self.passenger_manifest), 
      self.revenue,
      fmt.format("Passenger Name", "Seat#", "Price"), 
      "\n".join([str(p) for p in self.passenger_manifest.values()]))
    
  def book_passenger(self, client):
    '''
    Books a passenger on a flight. Assigns seat number, and creates a FlightPassenger object. Returns the FlightPassenger object or None if flight could not be booked
    
    :param client: client to book on flight
    :type client: Client
    '''
    # Make sure there is room on the flight
    if not self.available_seats:
      print >> stderr, "No available room on:", self.flightno, self.route_key
      return None
      
    if self.passenger_manifest.has_key(client.name):
      print >> stderr, client.name, "is already booked on:", self.flightno, self.route_key
      return None
    
    passenger = FlightPassenger(client, self)
    self.passenger_manifest[passenger.client.name] = passenger
    
    print >> stderr, client.name, "booked on:", self.flightno, self.route_key
    
    return passenger
    
  def remove_passenger(self, passenger):
    '''
    Removes a passenger from the flight manifest, and makes seat available again.
    
    :param passenger: passenger to be removed
    :type passenger: FlightPassenger
    '''
    self.available_seats.append(passenger.seat)
    del self.passenger_manifest[passenger.client.name]
    
    print >> stderr, passenger.client.name, "removed from:", self.flightno, self.route_key
    
    return None
    
  def change_price(self, price):
    '''
    Changes price of flight to the new value
    
    :param price: new price for flight
    :type price: str or unicode
    '''
    old = self.price
    self.price = float(price)
    print >> stderr, "Price of flight", self.flightno, self.route_key, "changed from", "$" + str(old), "to", "$" + str(self.price)
    