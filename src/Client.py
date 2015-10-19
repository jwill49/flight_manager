from sys import stderr

class Client:
  def __init__(self, name):
    self.name = name
    self.itinerary = {} # Mapping from SRC,DST ==> FlightPassenger
  
  def book_flight(self, flight):
    '''
    Book a client on the given flight.
    
    :param flight: Flight to book Client on
    :type flight: Flight
    '''
    passenger = flight.book_passenger(self)
    
    if passenger is not None:
      self.itinerary[flight.route_key] = passenger
    
  def cancel_flight(self, flight):
    '''
    Removes client a given flight. Returns the number of flights in client's itinerary.
    
    :param flight: Flight to book Client on
    :type flight: Flight
    '''
    if self.itinerary.has_key(flight.route_key):
      passenger = self.itinerary[flight.route_key]
      passenger.remove_from_flight()
      del self.itinerary[flight.route_key]
      del passenger
    
    return len(self.itinerary)
    
  def process_refund(self, amt):
    """
    Refund the specified amt to the client. Client accounts are not fully implemented, but here we'd use payment processing API, e.g. Braintree
    """
    print >> stderr, "$" + str(amt), "refunded to", self.name