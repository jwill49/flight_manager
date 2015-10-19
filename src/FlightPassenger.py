from sys import stderr
from shared import fmt

class FlightPassenger:
  def __init__(self, client, flight):
    self.client = client
    self.flight = flight
    self.seat = flight.available_seats.popleft()
    self.price = flight.price
    self.flight.revenue += flight.price
    
  # def __del__(self):
  #   self.flight.remove_passenger(self)
  #   self.client.process_refund(self.price)
  #   self.flight.revenue -= self.price
  
  def __str__(self):
    return fmt.format(self.client.name, str(self.seat), "$" + str(self.price))
    
  def remove_from_flight(self):
    """
    Caught a bug where I did not remove all references to object, in which the object will not be garbage collected. So this is a quick and dirty fix
    """
    self.flight.remove_passenger(self)
    self.client.process_refund(self.price)
    self.flight.revenue -= self.price